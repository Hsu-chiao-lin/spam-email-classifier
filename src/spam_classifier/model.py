"""Spam classification model."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, 
    f1_score, roc_auc_score, confusion_matrix
)

class SpamClassifier:
    """Logistic regression classifier for spam detection."""
    
    def __init__(
        self,
        C=1.0,
        class_weight="balanced",
        solver="liblinear",
        random_state=42
    ):
        self.model = LogisticRegression(
            C=C,
            class_weight=class_weight,
            solver=solver,
            random_state=random_state
        )
    
    def fit(self, X, y):
        """Train the classifier."""
        self.model.fit(X, y)
        return self
    
    def predict(self, X):
        """Predict spam (1) or ham (0)."""
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get probability estimates."""
        return self.model.predict_proba(X)
    
    def evaluate(self, X, y_true):
        """Compute multiple evaluation metrics."""
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)[:, 1]  # Prob of spam
        
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1": f1_score(y_true, y_pred),
            "roc_auc": roc_auc_score(y_true, y_proba),
            "confusion_matrix": confusion_matrix(y_true, y_pred)
        }
        
        return metrics