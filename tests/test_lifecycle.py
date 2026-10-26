import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lifecycle_agent.review import review_diff  # noqa: E402
from lifecycle_agent.deploy import make_manifest  # noqa: E402
from lifecycle_agent.monitor import probe, build_monitor_config  # noqa: E402
from lifecycle_agent.report import render  # noqa: E402

CLEAN = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,2 +1,3 @@
 import os
+def add(a, b):
+    return a + b
"""

BAD = """diff --git a/app.py b/app.py
--- a/app.py
+++ b/app.py
@@ -1,1 +1,3 @@
 x = 1
+api_key = "sk_live_abcdefghijkl"
+result = eval(user_input)
"""

SOL = """diff --git a/Vault.sol b/Vault.sol
--- a/Vault.sol
+++ b/Vault.sol
@@ -1,1 +1,2 @@
 contract Vault {}
+require(tx.origin == owner);
"""


class ReviewTests(unittest.TestCase):
    def test_clean_diff_passes(self):
        r = review_diff(CLEAN)
        self.assertFalse(r["blocking"])
        self.assertEqual(r["findings"], [])
        self.assertEqual(r["score"], 100)

    def test_secret_and_eval_are_flagged(self):
        r = review_diff(BAD)
        rules = {f["rule"] for f in r["findings"]}
        self.assertIn("hardcoded-secret", rules)
        self.assertIn("eval-use", rules)
        self.assertTrue(r["blocking"])

    def test_line_numbers_point_at_added_lines(self):
        r = review_diff(BAD)
        secret = next(f for f in r["findings"] if f["rule"] == "hardcoded-secret")
        self.assertEqual(secret["line"], 2)
        self.assertEqual(secret["file"], "app.py")

    def test_solidity_tx_origin_is_blocking(self):
        r = review_diff(SOL)
        self.assertTrue(any(f["rule"] == "tx-origin" for f in r["findings"]))
        self.assertTrue(r["blocking"])


class DeployTests(unittest.TestCase):
    def test_blocked_review_does_not_deploy(self):
        m = make_manifest(review_diff(BAD), env_name="staging", commit_sha="abc123")
        self.assertFalse(m["deploy"])

    def test_clean_review_deploys_with_monitor(self):
        m = make_manifest(review_diff(CLEAN), env_name="production", commit_sha="abcdef1234567890",
                          image="app", project="g/p")
        self.assertTrue(m["deploy"])
        self.assertEqual(m["image"], "app:abcdef123456")
        self.assertEqual(m["replicas"], 2)
        self.assertEqual(len(m["monitor"]["alerts"]), 3)


class MonitorTests(unittest.TestCase):
    def test_probe_without_url_is_skipped(self):
        self.assertFalse(probe("")["checked"])

    def test_probe_unreachable_is_data_not_crash(self):
        r = probe("http://127.0.0.1:9/health", timeout=2)
        self.assertTrue(r["checked"])
        self.assertFalse(r["ok"])

    def test_config_has_alerts(self):
        self.assertIn("alerts", build_monitor_config("staging"))


class ReportTests(unittest.TestCase):
    def test_report_mentions_block(self):
        review = review_diff(BAD)
        manifest = make_manifest(review)
        body = render(review, manifest, {"checked": False, "detail": "no DEPLOY_URL set"})
        self.assertIn("BLOCKING", body)
        self.assertIn("Deploy: skipped", body)


if __name__ == "__main__":
    unittest.main()
