"""Data loading and preprocessing utilities."""
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

class SpamDataset:
    """Handler for loading and preprocessing the SMS spam dataset."""
    
    def __init__(self, data_dir: Path = None):
        if data_dir is None:
            data_dir = Path(__file__).parent.parent.parent / "data"
        self.data_dir = data_dir
        self.raw_path = data_dir / "raw" / "sms_spam_no_header.csv"
    
    def load_raw(self) -> pd.DataFrame:
        """Load the raw dataset and add headers."""
        df = pd.read_csv(self.raw_path, names=["label", "text"])
        return df
    
    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply basic preprocessing to the text and labels."""
        # Convert labels to binary
        df["label"] = (df["label"] == "spam").astype(int)
        
        # Clean text
        df["text"] = df["text"].str.lower()
        df["text"] = df["text"].str.strip()
        
        return df
    
    def load_split(self, test_size=0.15, val_size=0.15, random_state=42):
        """Load and split the dataset into train/val/test."""
        df = self.load_raw()
        df = self.preprocess(df)
        
        # First split: train + val vs test
        train_val, test = train_test_split(
            df, test_size=test_size, stratify=df["label"], 
            random_state=random_state
        )
        
        # Second split: train vs val
        val_ratio = val_size / (1 - test_size)
        train, val = train_test_split(
            train_val, test_size=val_ratio, 
            stratify=train_val["label"], random_state=random_state
        )
        
        return train, val, test