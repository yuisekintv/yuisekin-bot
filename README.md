# Development

- `pip install -r`

# Testing

- `pytest -vv`

# Heroku

- `git push origin main`

# GCP Cloud Run

- `gcloud builds submit --tag gcr.io/yuiseki-development/slack-bot`
- `gcloud run deploy slack-bot --image gcr.io/yuiseki-development/slack-bot --platform managed`
