----
id: 0003
title: "Spam email classification (baseline: logistic regression)"
authors: ["<your name> <you@example.com>"]
status: draft
created: 2025-11-03
----

# Summary

This proposal describes building a spam email (SMS) classification pipeline using classical machine learning. The primary baseline model will be logistic regression trained on the SMS spam dataset referenced below. The goal of Phase 1 is to produce a reproducible baseline, evaluation metrics, and a small, testable codebase. Later phases are placeholders for expansion (feature engineering, model comparisons, deployment, monitoring).

# Motivation

Spam detection is a common NLP classification task and provides a useful, self-contained project for practicing dataset preparation, modeling, evaluation, and reproducible workflows. A simple, interpretable model such as logistic regression gives a strong baseline and helps identify downstream needs (feature engineering, class imbalance handling, data augmentation).

## Specification

Inputs: raw SMS messages (text) and optional metadata. Outputs: binary label (spam=1, ham=0) and a probability score for spam.

The Phase 1 implementation will provide a CLI and notebook to run the pipeline end-to-end, produce evaluation metrics (accuracy, precision, recall, F1, ROC-AUC), and save model artifacts for inspection.

# Data

Baseline dataset (SMS spam dataset):

https://raw.githubusercontent.com/PacktPublishing/Hands-On-Artificial-Intelligence-for-Cybersecurity/refs/heads/master/Chapter03/datasets/sms_spam_no_header.csv

Notes:
- Verify license and usage restrictions for this dataset before publishing derived work.
- The dataset is a simple CSV typically containing two columns: label (ham/spam) and message text.

# Phase 1 — baseline

Goal: produce a reproducible baseline classifier using logistic regression and measured evaluation metrics.

Planned steps:

1. Data acquisition
   - Download the CSV from the URL above and store it under `data/raw/sms_spam_no_header.csv`.
   - Add a short script `scripts/fetch_data.py` or PowerShell script to fetch and cache the dataset.

2. Preprocessing
   - Load CSV and add headers if missing: `label,text`.
   - Map labels to binary (ham=0, spam=1).
   - Basic cleaning: lowercasing, remove excessive whitespace, optionally strip URLs and non-alphanumeric characters.
   - Split dataset into train/validation/test (suggested 70/15/15 or stratified split to keep class balance).

3. Feature extraction
   - Baseline: TF-IDF vectorization of message text (scikit-learn `TfidfVectorizer`). Limit vocabulary size (e.g., 10k tokens) and consider n-grams (1,2).

4. Model
   - Train a logistic regression classifier (scikit-learn `LogisticRegression` with solver='liblinear' or 'saga' for L1/L2 experiments).
   - Note: earlier drafts mentioned SVM — we prioritize logistic regression as an interpretable baseline here; SVM can be a Phase N comparison.

5. Evaluation
   - Metrics: accuracy, precision, recall, F1, ROC-AUC. Report per-class precision/recall; report confusion matrix.
   - Save evaluation reports to `results/phase1/` and log model artifacts to `models/phase1/`.

6. Reproducibility & tests
   - Provide a notebook `notebooks/phase1_baseline.ipynb` demonstrating the pipeline end-to-end.
   - Add lightweight unit tests for preprocessing and a smoke test that trains on a tiny subset and verifies the pipeline runs.

7. Scripts & CLI
   - Provide a small CLI entrypoint `python -m spam_classifier train --config config/phase1.yaml` and `evaluate` command.

Acceptance criteria

- A trained logistic regression model and evaluation report exist in `models/phase1/` and `results/phase1/`.
- A reproducible notebook that walks through dataset download, preprocessing, training, and evaluation.
- Unit tests covering preprocessing and a smoke train run pass locally (CI-ready).
- Baseline metrics recorded; no strict threshold required yet, but aim for reasonable F1 (>0.80 is a useful target depending on dataset balance — this is flexible).

# PhaseN placeholders

Phase 2 — feature engineering and class imbalance handling (placeholder)

Phase 3 — model comparison: SVM, random forest, gradient boosting (placeholder)

Phase 4 — lightweight deployment (e.g., Dockerized microservice and an inference endpoint) (placeholder)

Phase 5 — monitoring and fairness/robustness checks (placeholder)

# Implementation plan & files to add

- `data/` — `raw/` and `processed/` placeholders and `.gitignore` rules to avoid committing large datasets.
- `scripts/fetch_data.py` — script to download and cache the CSV.
- `src/spam_classifier/` — package with modules: `data.py`, `features.py`, `model.py`, `cli.py`.
- `notebooks/phase1_baseline.ipynb` — reproducible workflow and visualizations.
- `tests/` — unit tests for preprocessing, small integration smoke test.
- `requirements.txt` or `pyproject.toml` with minimal deps: scikit-learn, pandas, numpy, pytest.

# Timeline

Estimate: Phase 1 minimal baseline can be implemented in 1-2 days of focused work (including tests and notebook). Iterative improvements and comparisons in later phases will take additional time.

# Risks and mitigations

- Data license: verify dataset license before publishing derived artifacts. Mitigation: confirm and document license in `data/README.md`.
- False positives: spam classifiers can mistakenly block legitimate messages. Mitigation: measure precision/recall; tune threshold; consider human-in-the-loop.
- Class imbalance: many spam datasets are imbalanced; mitigate with stratified splits and class-weighted learning or resampling.

# Ethical considerations

Be careful when publishing or deploying models that automatically filter or delete messages. Consider transparency, appeal mechanisms, and conservative deployment (e.g., flagging rather than deleting).

# Notes

If you'd like, I can implement Phase 1 now: scaffold the repository layout, add a `requirements.txt`, implement the data fetch script, implement preprocessing and training code, add the notebook, run a smoke test, and open a feature branch for review.
