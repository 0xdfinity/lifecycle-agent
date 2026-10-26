"""Stage 3: monitoring. Builds alert rules and probes the deployed health URL."""
import json
import os
import sys
import urllib.error
import urllib.request


def build_monitor_config(env_name="staging"):
    return {
        "health_url": os.environ.get("DEPLOY_URL", "") or None,
        "probe_interval_s": 60,
        "alerts": [
            {"name": "http-5xx-rate", "threshold": "> 2% over 5m", "severity": "critical"},
            {"name": "p95-latency", "threshold": "> 800ms over 5m", "severity": "warning"},
            {"name": "health-check-failing", "threshold": "2 consecutive failures", "severity": "critical"},
        ],
        "env": env_name,
    }


def probe(url, timeout=10):
    """Return a dict describing one health probe. Never raises."""
    if not url:
        return {"checked": False, "ok": None, "detail": "no DEPLOY_URL set, probe skipped"}
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return {"checked": True, "ok": 200 <= resp.status < 300, "status": resp.status,
                    "url": url}
    except urllib.error.HTTPError as e:
        return {"checked": True, "ok": False, "status": e.code, "url": url}
    except Exception as e:  # network errors are data, not crashes
        return {"checked": True, "ok": False, "status": None, "url": url, "detail": str(e)[:200]}


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("DEPLOY_URL", "")
    print(json.dumps(probe(url), indent=2))
