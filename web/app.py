import streamlit as st
from pathlib import Path
import json

from src.spam_classifier.pipeline import load_pipeline, train_and_save_pipeline, predict_texts

st.set_page_config(page_title="Spam SMS Demo", layout="centered")
st.title("Spam SMS Classifier — Demo")

# Ensure model exists
model = load_pipeline()
if model is None:
    with st.spinner("Training baseline model (this may take a minute)..."):
        model = train_and_save_pipeline()
    st.success("Model trained and saved.")

st.sidebar.header("Demo options")
show_metrics = st.sidebar.checkbox("Show baseline metrics (if available)", value=True)

col1, col2 = st.columns([3,2])
with col1:
    st.subheader("Single message classification")
    text = st.text_area("Enter SMS text to classify:", height=120)
    if st.button("Predict"):
        if not text.strip():
            st.warning("Please enter some text to classify.")
        else:
            preds, probs = predict_texts([text])
            label = "SPAM" if preds[0] == 1 else "HAM"
            st.write(f"Prediction: **{label}**")
            st.write(f"Spam probability: **{probs[0]:.3f}**")

with col2:
    st.subheader("Batch upload")
    uploaded = st.file_uploader("Upload a CSV with a `text` column", type=["csv"]) 
    if uploaded:
        import pandas as pd
        df = pd.read_csv(uploaded)
        if "text" not in df.columns:
            st.error("CSV must contain a 'text' column")
        else:
            preds, probs = predict_texts(df["text"].astype(str).tolist())
            df["pred"] = preds
            df["spam_prob"] = probs
            st.dataframe(df.head(50))
            st.download_button("Download predictions CSV", df.to_csv(index=False).encode("utf-8"), file_name="predictions.csv")

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
st.markdown("Built with scikit-learn and Streamlit — model retrains automatically if not found.")
