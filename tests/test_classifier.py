"""Test the spam classifier pipeline."""
import pytest
import pandas as pd
from pathlib import Path

from spam_classifier.data import SpamDataset
from spam_classifier.features import TextFeaturizer
from spam_classifier.model import SpamClassifier

@pytest.fixture
def sample_data():
    """Create a tiny dataset for testing."""
    data = {
        "label": ["ham", "spam", "ham", "spam"],
        "text": [
            "hello how are you",
            "win free money now",
            "meeting at 3pm",
            "claim your prize!!!"
        ]
    }
    return pd.DataFrame(data)

def test_preprocessing(sample_data):
    """Test data preprocessing."""
    dataset = SpamDataset()
    df = dataset.preprocess(sample_data)
    
    assert "label" in df.columns
    assert "text" in df.columns
    assert df["label"].dtype == "int64"
    assert (df["label"] == 1).sum() == 2  # Two spam messages

def test_feature_extraction(sample_data):
    """Test TF-IDF feature extraction."""
    featurizer = TextFeaturizer(max_features=100)
    X = featurizer.fit_transform(sample_data["text"])
    
    assert X.shape[0] == 4  # Four messages
    assert X.shape[1] <= 100  # Max features
    assert isinstance(featurizer.vocabulary_, dict)

def test_model_training(sample_data):
    """Test end-to-end training pipeline."""
    # Preprocess
    dataset = SpamDataset()
    df = dataset.preprocess(sample_data)
    
    # Extract features
    featurizer = TextFeaturizer(max_features=100)
    X = featurizer.fit_transform(df["text"])
    
    # Train
    classifier = SpamClassifier()
    classifier.fit(X, df["label"])
    
    # Predict
    y_pred = classifier.predict(X)
    assert len(y_pred) == 4
    
    # Evaluate
    metrics = classifier.evaluate(X, df["label"])
    assert 0 <= metrics["accuracy"] <= 1
    assert "confusion_matrix" in metrics