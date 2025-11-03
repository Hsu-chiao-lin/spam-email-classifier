# Entrypoint for Streamlit Community Cloud (and other hosts that look for a root app file)
# This simply imports the actual app implementation under web/app.py which defines the Streamlit UI.
from web import app  # noqa: F401
