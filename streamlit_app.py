
"""Entrypoint for Streamlit Community Cloud (self-contained).

This file contains a minimal Streamlit app inline (old working style)
to avoid import path issues in some deployment environments.
"""

from pathlib import Path
import sys
import json
import streamlit as st

# Ensure both repo root and src/ are on sys.path (src first)
REPO_ROOT = Path(__file__).parent
SRC_PATH = REPO_ROOT / "src"
if SRC_PATH.exists() and str(SRC_PATH) not in sys.path:
	sys.path.insert(0, str(SRC_PATH))
if str(REPO_ROOT) not in sys.path:
	sys.path.insert(0, str(REPO_ROOT))

from src.spam_classifier.pipeline import (
	load_pipeline,
	train_and_save_pipeline,
	predict_texts,
)


st.set_page_config(page_title="2025 Spam Email Demo", layout="centered")
st.title("2025 Spam Email Classification Demo")

st.markdown(
	"""
This demo shows a simple spam classifier trained on SMS messages. You can:
1. Enter a single message to classify
2. Upload a CSV file with multiple messages
"""
)

# Ensure model exists (may use fallback inside load_pipeline)
model = load_pipeline()
if model is None:
	with st.spinner("Training baseline model (this may take a minute)..."):
		model = train_and_save_pipeline()
	st.success("Model trained and saved.")

st.sidebar.header("Demo options")
show_metrics = st.sidebar.checkbox("Show baseline metrics (if available)", value=True)

col1, col2 = st.columns([3, 2])
with col1:
	st.subheader("Single message classification")
	text = st.text_area("Enter SMS text to classify:", height=120)
	if st.button("Predict"):
		if not text.strip():
			st.warning("Please enter some text to classify.")
		else:
			preds, probs = predict_texts([text])
			label = "SPAM" if int(preds[0]) == 1 else "HAM"
			st.write(f"Prediction: **{label}**")
			try:
				st.write(f"Spam probability: **{float(probs[0]):.3f}**")
			except Exception:
				pass

with col2:
	st.subheader("Batch upload")
	uploaded = st.file_uploader("Upload a CSV with a `text` column", type=["csv"]) 
	if uploaded:
		import pandas as pd
		try:
			df = pd.read_csv(uploaded)
		except Exception as e:
			st.error(f"Couldn't read CSV: {e}")
			df = None
		if df is not None:
			if "text" not in df.columns:
				st.error("CSV must contain a 'text' column")
			else:
				preds, probs = predict_texts(df["text"].astype(str).tolist())
				df["pred"] = ["SPAM" if int(p) == 1 else "HAM" for p in preds]
				try:
					df["spam_prob"] = [float(p) for p in probs]
				except Exception:
					df["spam_prob"] = [1.0 if int(p) == 1 else 0.0 for p in preds]
				st.dataframe(df.head(50))
				st.download_button(
					"Download predictions CSV",
					df.to_csv(index=False).encode("utf-8"),
					file_name="predictions.csv",
				)

if show_metrics:
	metrics_path = Path("results") / "phase1" / "metrics.json"
	if metrics_path.exists():
		with open(metrics_path, "r", encoding="utf-8") as f:
			metrics = json.load(f)
		st.subheader("Baseline Metrics (from Phase 1)")
		st.write(metrics.get("val", {}))
	else:
		st.info("No metrics file found yet. Run training to generate metrics.")

st.markdown("---")
st.markdown(
	"""
### About
- Built with scikit-learn and Streamlit
- Model retrains automatically if not found
- View the [source code](https://github.com/Hsu-chiao-lin/spam-email-classifier)
"""
)
