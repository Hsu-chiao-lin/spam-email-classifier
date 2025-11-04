"""Entrypoint for Streamlit Community Cloud.

This file keeps the root app file minimal so Streamlit Cloud will run it.
It imports the actual app implementation from `web/app.py`.
"""

from web import app  # noqa: F401
