# Life After Code: demo video script (target 2m40s, hard limit 3:00)

No copyrighted music, no third-party trademarks beyond the GitLab name and logo. Record the screen at 1080p. Keep narration under 380 words.

Shot 1 (0:00 to 0:15). Title card: "Life After Code". Narration: "Code is written. Now it has to get to production, and that path is mostly manual. Life After Code automates it on GitLab."

Shot 2 (0:15 to 0:35). The GitLab project page, the README, and the MIT license visible at the top. Narration: "Everything here is public and MIT licensed. The pipeline is in .gitlab-ci.yml."

Shot 3 (0:35 to 1:00). Open a merge request that adds a hardcoded API key and eval(). Narration: "I open a merge request with a hardcoded secret and an eval call."

Shot 4 (1:00 to 1:25). Pipeline runs: review stage fails the gate. Show review.json on screen with the findings and line numbers. Narration: "The review stage flags both, with file and line. High severity blocks deployment, so the deploy job is skipped."

Shot 5 (1:25 to 1:55). Fix the MR: move the key to a CI variable, remove eval. Push. Pipeline reruns. Show green review, build tests passing (10 of 10), and deploy-manifest.json with the image tag and monitor config. Narration: "I fix it and push. The tests pass, the review passes, and the deploy manifest is written for staging with alert rules."

Shot 6 (1:55 to 2:20). Show the monitor job output and the Duo flow in the project under AI > Flows. Narration: "The monitor stage probes the health URL. GitLab Duo runs a review agent and a summary agent through a custom flow, triggered from the merge request."

Shot 7 (2:20 to 2:40). The MR note posted by the report stage with the lifecycle report. Narration: "The lifecycle report lands on the merge request. Review, deploy, health, and the next action in one place. Life After Code. Thanks for watching."

Recording checklist: pipeline history visible in the first 30 seconds of the pipeline shot; do not show tokens or the GITLAB_TOKEN value; keep the video under 3:00 when exported.
