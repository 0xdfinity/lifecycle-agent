Optional Google Cloud Run deploy (bonus eligibility, up to 0.2 points).

Untested live: needs your GCP project and billing enabled.

gcloud auth login
gcloud config set project YOUR_PROJECT_ID
gcloud run deploy life-after-code --source ../.. --region us-central1 --allow-unauthenticated

Then set DEPLOY_URL in GitLab CI/CD variables to the Cloud Run URL so the monitor stage probes it.
