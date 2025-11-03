"""Pipeline utilities: train, save, load a sklearn pipeline for spam classification."""
from pathlib import Path
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from .data import SpamDataset

MODELS_DIR = Path(__file__).parent.parent / "models" / "phase1"
MODELS_DIR.mkdir(parents=True, exist_ok=True)
MODEL_PATH = MODELS_DIR / "pipeline.joblib"


def train_and_save_pipeline(max_features=10000, ngram_range=(1,2), C=1.0):
    dataset = SpamDataset()
    train_df, val_df, test_df = dataset.load_split()
    X_train = train_df["text"].tolist()
    y_train = train_df["label"].tolist()

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(max_features=max_features, ngram_range=ngram_range, min_df=1)),
            ("clf", LogisticRegression(C=C, class_weight="balanced", solver="liblinear", random_state=42)),
        ]
    )
    pipeline.fit(X_train, y_train)
    joblib.dump(pipeline, MODEL_PATH)
    return pipeline


def load_pipeline():
    if MODEL_PATH.exists():
        return joblib.load(MODEL_PATH)
    return None


def predict_texts(texts):
    pipe = load_pipeline()
    if pipe is None:
        pipe = train_and_save_pipeline()
    preds = pipe.predict(texts)
    probs = pipe.predict_proba(texts)[:, 1]
    return preds, probs
