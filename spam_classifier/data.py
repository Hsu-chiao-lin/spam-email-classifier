"""Compatibility wrapper for `spam_classifier.data` pointing to `src.spam_classifier.data`.

This file simply re-exports the public symbols from the implementation under `src/`.
"""
from src.spam_classifier.data import *  # noqa: F401,F403
