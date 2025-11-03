"""Command-line interface for spam classifier."""
import argparse
import json
from pathlib import Path

from .data import SpamDataset
from .features import TextFeaturizer
from .model import SpamClassifier

def train(args):
    """Train a new spam classifier."""
    # Load and split data
    dataset = SpamDataset()
    train_df, val_df, test_df = dataset.load_split(
        test_size=args.test_size,
        val_size=args.val_size
    )
    
    # Extract features
    featurizer = TextFeaturizer(
        max_features=args.max_features,
        ngram_range=(1, args.max_ngram)
    )
    
    X_train = featurizer.fit_transform(train_df["text"])
    X_val = featurizer.transform(val_df["text"])
    X_test = featurizer.transform(test_df["text"])
    
    # Train model
    classifier = SpamClassifier(
        C=args.regularization,
        class_weight="balanced"
    )
    classifier.fit(X_train, train_df["label"])
    
    # Evaluate
    results = {
        "train": classifier.evaluate(X_train, train_df["label"]),
        "val": classifier.evaluate(X_val, val_df["label"]),
        "test": classifier.evaluate(X_test, test_df["label"])
    }
    
    # Save results
    output_dir = Path("results") / "phase1"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Convert numpy arrays and numpy types to native Python types for JSON
    def _make_json_serializable(obj):
        if isinstance(obj, dict):
            return {k: _make_json_serializable(v) for k, v in obj.items()}
        if hasattr(obj, "tolist"):
            return obj.tolist()
        try:
            return float(obj)
        except Exception:
            return obj

    serializable = _make_json_serializable(results)
    with open(output_dir / "metrics.json", "w") as f:
        json.dump(serializable, f, indent=2)
    
    print("\nResults saved to results/phase1/metrics.json")
    print("\nValidation metrics:")
    for metric, value in results["val"].items():
        if metric != "confusion_matrix":
            print(f"{metric}: {value:.3f}")

def main():
    parser = argparse.ArgumentParser(description="Train spam classifier")
    parser.add_argument("--test-size", type=float, default=0.15)
    parser.add_argument("--val-size", type=float, default=0.15)
    parser.add_argument("--max-features", type=int, default=10000)
    parser.add_argument("--max-ngram", type=int, default=2)
    parser.add_argument("--regularization", type=float, default=1.0)
    
    args = parser.parse_args()
    train(args)

if __name__ == "__main__":
    main()