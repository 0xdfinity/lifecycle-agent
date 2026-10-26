"""Stage 2: gate on the review, then write a deploy manifest and monitoring config.

Deploy is a manifest, not a live rollout: the CI job publishes the artifact and this
file is what a real environment (Cloud Run, Kubernetes, a VM) would apply.
"""
import json
import os
import sys
import time

from lifecycle_agent.monitor import build_monitor_config


def make_manifest(review, env_name="staging", commit_sha=None, image="app", project=None):
    sha = commit_sha or os.environ.get("CI_COMMIT_SHA", "local")
    if review["blocking"]:
        return {"deploy": False, "reason": "blocked by high-severity review findings",
                "env": env_name, "commit": sha}
    return {
        "deploy": True,
        "env": env_name,
        "commit": sha,
        "image": f"{image}:{sha[:12]}",
        "project": project or os.environ.get("CI_PROJECT_PATH", "local/project"),
        "replicas": 2 if env_name == "production" else 1,
        "created_at": int(time.time()),
        "monitor": build_monitor_config(env_name),
    }


if __name__ == "__main__":
    review_path, out_path = sys.argv[1], sys.argv[2]
    env_name = sys.argv[3] if len(sys.argv) > 3 else "staging"
    with open(review_path, encoding="utf-8") as fh:
        review = json.load(fh)
    manifest = make_manifest(review, env_name=env_name)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)
    print(json.dumps({"deploy": manifest["deploy"], "reason": manifest.get("reason", "ok")}))
