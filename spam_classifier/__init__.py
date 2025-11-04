"""Top-level compatibility package exposing the library under `spam_classifier`.

This package re-exports the implementation under `src/spam_classifier` so tests
and older imports that use `spam_classifier` work without modifying PYTHONPATH.
"""

from . import data, features, model  # noqa: F401

__all__ = ["data", "features", "model"]
