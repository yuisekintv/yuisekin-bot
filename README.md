# Heroku

- `git push origin main`

# GCP Cloud Run

- `gcloud builds submit --tag gcr.io/yuiseki-development/slack-bot`
- `gcloud run deploy --image gcr.io/yuiseki-development/slack-bot --platform managed`