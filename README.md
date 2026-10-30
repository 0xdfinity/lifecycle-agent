# Life After Code

An agent that takes a commit or merge request and runs the rest of the post-code lifecycle on GitLab: AI-assisted review, a quality gate, build, deploy, monitoring, and a report posted back to the MR.

Built for the GitLab Transcend hackathon; MIT licensed.

## What it does

1. Review: diffs the MR against its target branch and scores added lines for secrets, private keys, eval, tx.origin (Solidity), unchecked low-level calls, debug leftovers and missing tests. High-severity findings block the pipeline.
2. Build and test: runs the unit suite and packages the artifact.
3. Deploy: if the review passes, writes a deploy manifest (image tag, replicas, monitoring config) for the staging environment. A blocked review produces a manifest that says deploy: false.
4. Monitor: writes alert rules (5xx rate, p95 latency, health failing) and probes DEPLOY_URL when set.
5. Report: writes lifecycle-report.md and posts it as a note on the merge request through the GitLab API.

GitLab Duo Agent Platform: `.gitlab/duo/flows/lifecycle.yml` is a custom flow (flow registry v1 syntax) that adds an LLM reviewer and summary agent on top of the rule engine. It is triggered by mentioning or assigning the flow's service account on a merge request.

## Run locally

    python3 -m unittest discover -s tests -v
    git diff main...HEAD | python3 -m lifecycle_agent.review -

No dependencies beyond the Python 3 standard library.

## CI/CD

.gitlab-ci.yml defines five stages: review, build, deploy_staging, monitor, report. Each stage produces artifacts (review.json, deploy-manifest.json, health.json, lifecycle-report.md) that show up in the pipeline history.

## Environment variables

- DEPLOY_URL: health URL of the deployed app (optional, probe skipped if unset).
- GITLAB_TOKEN: a project access token with api scope, used to post the MR note (optional).

## License and third-party code

MIT, see LICENSE. The code is original. It uses only the Python standard library. The GitLab Duo flow YAML follows GitLab's documented custom flow format.
