"""Stage 4: write a Markdown lifecycle report and post it to the merge request if possible."""
import json
import os
import sys
import urllib.request


def render(review, manifest, probe_result):
    lines = ["## Life After Code: lifecycle report", ""]
    lines.append(f"Review score: {review['score']}/100 ({len(review['findings'])} findings, "
                 f"{'BLOCKING' if review['blocking'] else 'no blocking issues'})")
    for f in review["findings"][:20]:
        lines.append(f"- [{f['severity']}] {f['rule']} at {f['file']}:{f['line']}: {f['message']}")
    lines.append("")
    if manifest.get("deploy"):
        lines.append(f"Deploy: shipped {manifest['image']} to {manifest['env']} "
                     f"({manifest['replicas']} replica(s)).")
    else:
        lines.append(f"Deploy: skipped. {manifest.get('reason')}")
    if probe_result.get("checked"):
        state = "healthy" if probe_result["ok"] else "UNHEALTHY"
        lines.append(f"Monitoring: health probe {state} (status {probe_result.get('status')}).")
    else:
        lines.append(f"Monitoring: {probe_result.get('detail')}. Alert rules were written.")
    return "\n".join(lines) + "\n"


def post_mr_note(body):
    """Post to the MR through the GitLab API when running in an MR pipeline. Returns a status string."""
    token = os.environ.get("GITLAB_TOKEN")
    project_id = os.environ.get("CI_PROJECT_ID")
    mr_iid = os.environ.get("CI_MERGE_REQUEST_IID")
    api = os.environ.get("CI_API_V4_URL", "https://gitlab.com/api/v4")
    if not (token and project_id and mr_iid):
        return "skipped: not an MR pipeline or GITLAB_TOKEN unset"
    url = f"{api}/projects/{project_id}/merge_requests/{mr_iid}/notes"
    req = urllib.request.Request(url, data=json.dumps({"body": body}).encode(),
                                 headers={"PRIVATE-TOKEN": token, "Content-Type": "application/json"},
                                 method="POST")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return f"posted MR note (HTTP {resp.status})"


if __name__ == "__main__":
    review = json.load(open(sys.argv[1], encoding="utf-8"))
    manifest = json.load(open(sys.argv[2], encoding="utf-8"))
    probe_result = json.load(open(sys.argv[3], encoding="utf-8"))
    body = render(review, manifest, probe_result)
    out = sys.argv[4] if len(sys.argv) > 4 else "lifecycle-report.md"
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(body)
    try:
        status = post_mr_note(body)
    except Exception as e:
        status = f"MR note failed: {e}"
    print(status)
