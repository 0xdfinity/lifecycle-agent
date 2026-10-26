"""Stage 1: review a unified diff (a commit or merge request) with deterministic rules.

This is the always-on reviewer. The GitLab Duo flow in .gitlab/duo/flows/lifecycle.yml
adds an LLM review on top when the flow is enabled in the project.
"""
import json
import re
import sys

RULES = [
    ("hardcoded-secret", "high", re.compile(r"(api[_-]?key|secret|token|password)\s*[=:]\s*['\"][^'\"]{8,}['\"]", re.I),
     "Looks like a hardcoded credential. Move it to a CI/CD variable."),
    ("private-key", "high", re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
     "Private key material in the diff."),
    ("eval-use", "medium", re.compile(r"\beval\s*\("),
     "eval() executes arbitrary code. Prefer a parser or an explicit dispatch table."),
    ("debugger", "low", re.compile(r"\b(console\.log|debugger|breakpoint\(\)|pdb\.set_trace)\b"),
     "Debug leftover."),
    ("todo-marker", "low", re.compile(r"\b(TODO|FIXME|XXX)\b"),
     "Unresolved TODO/FIXME added."),
    ("tx-origin", "high", re.compile(r"\btx\.origin\b"),
     "tx.origin used for authorization (Solidity). Use msg.sender."),
    ("unchecked-call", "medium", re.compile(r"\.call\{value"),
     "Low-level call with value. Check the return value and follow checks-effects-interactions."),
]


def parse_diff(diff_text):
    """Yield (file_path, line_number, added_line) for every added line."""
    path, lineno = None, 0
    for raw in diff_text.splitlines():
        if raw.startswith("+++ "):
            path = raw[4:].strip()
            if path.startswith("b/"):
                path = path[2:]
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) - 1 if m else 0
        elif raw.startswith("+") and not raw.startswith("+++"):
            lineno += 1
            yield path or "unknown", lineno, raw[1:]
        elif not raw.startswith("-"):
            lineno += 1


def review_diff(diff_text):
    findings = []
    for path, line, text in parse_diff(diff_text):
        for rule_id, severity, pattern, message in RULES:
            if pattern.search(text):
                findings.append({"rule": rule_id, "severity": severity,
                                 "file": path, "line": line, "message": message,
                                 "snippet": text.strip()[:160]})
    added = sum(1 for _ in parse_diff(diff_text))
    has_tests = any(re.search(r"^\+\+\+ .*(test|spec)", l, re.I) for l in diff_text.splitlines())
    if added > 40 and not has_tests:
        findings.append({"rule": "no-tests", "severity": "medium", "file": "-", "line": 0,
                         "message": f"{added} lines added with no test file touched.", "snippet": ""})
    weights = {"high": 3, "medium": 2, "low": 1}
    score = max(0, 100 - sum(weights[f["severity"]] * 10 for f in findings))
    blocking = any(f["severity"] == "high" for f in findings)
    return {"score": score, "blocking": blocking, "added_lines": added, "findings": findings}


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "-"
    text = sys.stdin.read() if src == "-" else open(src, encoding="utf-8").read()
    print(json.dumps(review_diff(text), indent=2))
