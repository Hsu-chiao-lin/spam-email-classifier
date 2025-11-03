# 2025 Spam Email Classification Demo

A spam classification demo using scikit-learn and Streamlit, featuring both single-message and batch classification capabilities.

## Live Demo

Visit the live demo at: [2025 Spam Email Demo](https://2025spamemail.streamlit.app/)

## Features

- Single message classification with probability scores
- Batch classification via CSV upload
- Model performance metrics display
- Automatic model training on first use
- Download predictions as CSV

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Hsu-chiao-lin/spam-email-classifier.git
   cd spam-email-classifier
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

## Project Structure

```
.
├── data/
│   └── raw/               # Raw SMS spam dataset
├── notebooks/             # Jupyter notebooks for analysis
├── src/
│   └── spam_classifier/   # Core ML implementation
├── tests/                 # Test files
├── web/                   # Streamlit app
└── requirements.txt       # Project dependencies
```

## Development

- Run tests: `pytest`
- Format code: `black .`
- Check OpenSpec proposals: `python scripts/spec_lint.py`

## License

MIT License

## Contributors

- Hsu-chiao-lin