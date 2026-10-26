# Publish steps (your GitLab account)

Prereqs: a GitLab.com account, git installed, the project folder at hackathon-gitlab/.

1. Create the project. On gitlab.com click New project, then Create blank project. Name it life-after-code. Visibility: Public. Do not add a README or license in the UI (the folder already has them). Click Create project and copy the HTTPS URL, for example https://gitlab.com/YOUR_USER/life-after-code.git.

2. Push the code. In a terminal inside hackathon-gitlab/:

    git remote add origin https://gitlab.com/YOUR_USER/life-after-code.git
    git branch -M main
    git push -u origin main

   Git will ask you to sign in. Use a personal access token as the password, not your account password.

3. Confirm the pipeline ran. Open Build > Pipelines in the project. You should see a pipeline with review, build, deploy_staging, monitor, report. If it shows "CI/CD yaml invalid", open Build > Pipeline editor and fix the message it shows.

4. Make a merge request for the demo. Create a branch, add a file with a fake key (for example password = "hunter2hunter2"), push it, then open a merge request into main. The review job should fail the gate and the pipeline history will show it. Then fix the file, push, and show the green run for the video.

5. Optional: turn on GitLab Duo. Project > Settings > General > Visibility, then the GitLab Duo section, enable GitLab Duo Agent Platform for the project. Then Project > AI > Flows > New flow. Paste the contents of .gitlab/duo/flows/lifecycle.yml into the Configuration editor, name it Life After Code Lifecycle, set Visibility to Private, and select Create flow. Enable it for the project. Test it by mentioning the flow's service account (shown on the flow page) in a merge request comment. The flow is a draft: if the editor reports a schema error, fix it using the message. The pipeline does not depend on the flow, so the submission still works without it.

6. Optional: post the MR report. Project > Settings > Access tokens, create a token with Developer role and api scope, then Settings > CI/CD > Variables, add GITLAB_TOKEN as masked. Without it the report stage still writes lifecycle-report.md as an artifact.

7. Optional: set DEPLOY_URL in Settings > CI/CD > Variables to a live health URL to make the monitor probe real.

8. Get the links for Devpost: the project URL, the pipelines URL (Build > Pipelines), and the MR URL that shows the failed then passed review.

9. Record the video from VIDEO_SCRIPT.md, under 3 minutes, and upload it to YouTube as public. Use Canva or any editor and keep the audio free of copyrighted music.

10. Submit at https://gitlab-transcend.devpost.com/. Paste DEVPOST.md, fill the three placeholders (repo, pipelines, video), and submit before the deadline. Verified deadline (gitlab-transcend.devpost.com/rules): submission period closes Oct 27, 2026 1:00pm UTC. Registration closes the same time, and GitLab contributor approval takes about 24 business hours, so register first. Google Cloud deployment is a bonus (up to 0.2 points), not a requirement; see deploy/gcp/README.md if you want it.
