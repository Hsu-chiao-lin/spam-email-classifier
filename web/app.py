import streamlit as st
from pathlib import Path
import json
from typing import List, Tuple

import pandas as pd

from src.spam_classifier.pipeline import load_pipeline, train_and_save_pipeline, predict_texts


st.set_page_config(page_title="2025 Spam Email Demo", layout="centered")
st.title("2025 Spam Email Classification Demo")

st.markdown(
    """
This demo shows a simple spam classifier trained on SMS messages. You can:
- Enter a single message to classify
- Upload a CSV file with multiple messages

Tips:
- Use the example buttons to try common spam/ham messages
"""
)


@st.cache_resource
def get_or_train_pipeline():
    """Load an existing pipeline or train and save a new one.

    Cached so the model isn't reloaded or retrained on every interaction.
    """
    pipe = load_pipeline()
    if pipe is None:
        pipe = train_and_save_pipeline()
    return pipe


def safe_predict(texts: List[str]) -> Tuple[List[int], List[float]]:
    """Call the pipeline predict functions and normalize outputs."""
    pipe = get_or_train_pipeline()
    # The existing predict_texts helper will also load/train if needed; use it for compatibility.
    preds, probs = predict_texts(texts)
    # Ensure lists and numeric types
    preds = [int(p) for p in preds]
    probs = [float(p) for p in probs]
    return preds, probs


def top_positive_tokens(pipe, n: int = 15) -> List[Tuple[str, float]]:
    """Return top tokens that increase the spam score (token, weight).

    Works with a Pipeline containing a TfidfVectorizer named 'tfidf' and a linear 'clf'.
    """
    try:
        tfidf = pipe.named_steps.get("tfidf")
        clf = pipe.named_steps.get("clf")
        if tfidf is None or clf is None:
            return []
        feature_names = list(tfidf.get_feature_names_out())
        coefs = clf.coef_[0]
        pairs = list(zip(feature_names, coefs))
        pairs.sort(key=lambda x: x[1], reverse=True)
        return pairs[:n]
    except Exception:
        return []


# Ensure / load model once and cache it
model = get_or_train_pipeline()


st.sidebar.header("Demo options")
show_metrics = st.sidebar.checkbox("Show baseline metrics (if available)", value=True)

# Example quick buttons
examples = [
    ("Free prize! Call now", "Congratulations! You have won a free prize. Call 0800-XXX now to claim."),
    ("Bank OTP", "Your OTP is 123456. Do not share this with anyone."),
    ("Dinner plan", "Hey, are we still on for dinner tonight?"),
]

col1, col2 = st.columns([3, 2])
with col1:
    st.subheader("Single message classification")
    example_cols = st.columns(len(examples))
    for (label, msg), c in zip(examples, example_cols):
        if c.button(label):
            st.session_state["input_text"] = msg

    text = st.text_area("Enter SMS text to classify:", value=st.session_state.get("input_text", ""), height=140)

    if st.button("Predict"):
        if not text.strip():
            st.warning("Please enter some text to classify.")
        else:
            with st.spinner("Classifying..."):
                preds, probs = safe_predict([text])
            label = "SPAM" if preds[0] == 1 else "HAM"
            st.metric("Prediction", label)
            st.write(f"Spam probability: **{probs[0]:.3f}**")

            # show top tokens if available
            tokens = top_positive_tokens(model, n=10)
            if tokens:
                st.markdown("**Top tokens that indicate SPAM (approx):**")
                st.write(
                    ", ".join([f"{t} ({w:.2f})" for t, w in tokens[:10]])
                )

with col2:
    st.subheader("Batch upload")
    uploaded = st.file_uploader("Upload a CSV with a `text` column (or `message`)", type=["csv"]) 
    if uploaded:
        try:
            df = pd.read_csv(uploaded)
        except Exception as e:
            st.error(f"Couldn't read CSV: {e}")
            df = None

        if df is not None:
            # try common column names
            col_candidates = [c for c in df.columns if c.lower() in ("text", "message", "body")]
            if not col_candidates:
                st.error("CSV must contain a 'text' or 'message' column")
            else:
                text_col = col_candidates[0]
                with st.spinner("Classifying batch..."):
                    preds, probs = safe_predict(df[text_col].astype(str).tolist())
                df["pred"] = ["SPAM" if p == 1 else "HAM" for p in preds]
                df["spam_prob"] = probs
                st.dataframe(df.head(50))
                csv_bytes = df.to_csv(index=False).encode("utf-8")
                st.download_button("Download predictions CSV", csv_bytes, file_name="predictions.csv")


if show_metrics:
    metrics_path = Path("results") / "phase1" / "metrics.json"
    if metrics_path.exists():
        with open(metrics_path, "r", encoding="utf-8") as f:
            metrics = json.load(f)
        st.subheader("Baseline Metrics (from Phase 1)")
        st.json(metrics.get("val", metrics))
    else:
        st.info("No metrics file found yet. Run training locally to generate metrics or wait for the first training run.")


st.markdown("---")
st.markdown(
    """
### About
- Built with scikit-learn and Streamlit
- Model retrains automatically if not found
- View the [source code](https://github.com/Hsu-chiao-lin/spam-email-classifier)
"""
)
