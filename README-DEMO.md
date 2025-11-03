# Demo: Spam SMS Classifier (Streamlit)

This demo runs a simple Streamlit app that loads or trains a baseline logistic regression pipeline and lets you classify SMS messages interactively.

Quick start (Windows PowerShell):

```powershell
python -m pip install -r requirements.txt
python scripts/fetch_data.py
# Run the Streamlit app
streamlit run web/app.py
```

Notes:
- The first run will train a baseline pipeline and save it to `models/phase1/pipeline.joblib`.
- Predictions can be made via the single-text input or by uploading a CSV with a `text` column.
- Metrics from Phase 1 (if present) are displayed in the sidebar.
