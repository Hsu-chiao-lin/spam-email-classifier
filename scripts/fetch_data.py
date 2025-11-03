"""Script to download and cache the SMS spam dataset."""
import os
import urllib.request
from pathlib import Path

# Dataset URL
DATASET_URL = "https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/refs/heads/master/Chapter03/datasets/sms_spam_no_header.csv"

# Local paths
DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
DATASET_PATH = RAW_DIR / "sms_spam_no_header.csv"

def download_dataset():
    """Download the SMS spam dataset if not already cached."""
    if DATASET_PATH.exists():
        print(f"Dataset already exists at {DATASET_PATH}")
        return
    
    print(f"Downloading dataset from {DATASET_URL}")
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        urllib.request.urlretrieve(DATASET_URL, DATASET_PATH)
        print(f"Dataset downloaded to {DATASET_PATH}")
    except Exception as e:
        print(f"Error downloading dataset: {e}")
        if DATASET_PATH.exists():
            DATASET_PATH.unlink()
        raise

if __name__ == "__main__":
    download_dataset()