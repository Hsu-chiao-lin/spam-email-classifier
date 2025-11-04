# Deploying the Spam SMS Streamlit demo

This repository contains a Streamlit demo under `web/app.py`. You can deploy it to Streamlit Community Cloud (recommended) or run locally.

## Prepare

1. Commit and push your repo to GitHub (the CI workflow will run tests on push).
2. Make sure `requirements.txt` is up to date (it includes Streamlit and other deps).

## Deploy to Streamlit Community Cloud (recommended)

1. Go to https://share.streamlit.io/ and sign in with your GitHub account.
2. Click "New app" and select the repository and branch (e.g., `main`).
3. For the "Main file path" set either:
   - `streamlit_app.py` (this repo includes a root entrypoint), or
   - `web/app.py` (the app is also available there).
4. Click "Deploy".

Notes:
- On first run the app will train a baseline model if `models/phase1/pipeline.joblib` is not present. That can take a minute. To make the live demo start instantly, pre-train locally and commit `models/phase1/pipeline.joblib` (check dataset license before committing derived artifacts).
- The repository includes a CI workflow in `.github/workflows/ci.yml` that runs tests and the spec-linter on each push.

## Local run (for testing)

```powershell
python -m pip install -r requirements.txt
python scripts/fetch_data.py

# Recommended (Cloud entrypoint)
streamlit run streamlit_app.py

# Alternate
# streamlit run web/app.py
```

## Advanced

- If you want automatic deployments elsewhere (Render, Railway, Docker), I can help scaffold a Dockerfile or a render/app.yaml.
