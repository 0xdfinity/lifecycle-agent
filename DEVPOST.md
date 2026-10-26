# Life After Code

Project name: Life After Code
Track: Path A (start fresh), GitLab Duo Agent Platform

Tagline: an agent that takes your merge request all the way from review to production and monitoring, and reports back on the MR.

What it does: you open a merge request. Life After Code reviews the diff, blocks it if it finds high-severity issues (hardcoded secrets, private keys, eval, tx.origin in Solidity), builds and tests it, deploys to staging only when the review passes, writes alert rules and probes the health URL, then posts a lifecycle report as a note on the merge request.

The problem: after code is written, the path to production is a chain of manual handoffs (review, pipeline babysitting, deploy, watching dashboards, reporting status). Most of that is mechanical and gets skipped under deadline pressure.

How GitLab is used:
- GitLab CI/CD: .gitlab-ci.yml runs the five stages on every merge request and on main. The pipeline history shows each run.
- GitLab Duo Agent Platform: a custom flow (.gitlab/duo/flows/lifecycle.yml) with a reviewer agent and a summary agent, triggered from the merge request by mentioning or assigning the flow service account.
- GitLab merge request API: the report is posted back to the MR so reviewers see the verdict where they already work.

What is real: the review engine, the deploy gate, the monitor probe and the report are tested (10 unit tests pass). The pipeline runs on the stock python image with no dependencies.

What is not included: the deploy stage writes a manifest, it does not roll out to a cloud provider. An optional Google Cloud Run deploy script is in deploy/gcp/ (bonus eligibility, untested live). A real environment would apply that manifest. Duo flow YAML must be validated in the GitLab UI before publishing.

Built with: Python 3 standard library, GitLab CI/CD, GitLab Duo Agent Platform custom flows.
License: MIT.

Repository: [paste your public GitLab URL]
Pipeline history: [paste the pipelines URL]
Demo video: [paste the YouTube URL, under 3 minutes]
