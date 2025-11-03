"""Feature extraction for text classification."""
from sklearn.feature_extraction.text import TfidfVectorizer

class TextFeaturizer:
    """Convert text to TF-IDF features."""
    
    def __init__(
        self, 
        max_features=10000,
        ngram_range=(1, 2),
        min_df=1,
        max_df=0.95
    ):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features,
            ngram_range=ngram_range,
            min_df=min_df,
            max_df=max_df
        )
    
    def fit(self, texts):
        """Learn vocabulary from training texts."""
        self.vectorizer.fit(texts)
        return self
    
    def transform(self, texts):
        """Convert texts to TF-IDF feature matrix."""
        return self.vectorizer.transform(texts)
    
    def fit_transform(self, texts):
        """Learn vocabulary and transform texts."""
        return self.vectorizer.fit_transform(texts)
    
    @property
    def vocabulary_(self):
        """Get the learned vocabulary."""
        return self.vectorizer.vocabulary_