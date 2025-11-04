
"""Entrypoint for Streamlit Community Cloud.

This file keeps the root app file minimal so Streamlit Cloud will run it.
It imports the actual app implementation from `web/app.py`.

We import via importlib after ensuring the repository root is first on
sys.path. This avoids conflicts with any third-party package named
``web`` that could shadow the local `web` directory on the deployment
environment.
"""

import sys
from pathlib import Path
import importlib

# Ensure repository root is on sys.path so local packages are preferred.
repo_root = Path(__file__).parent
src_path = repo_root / "src"

# Prepend src_path first so the real implementation under src/ is preferred
# over any top-level compatibility shims or third-party packages.
if src_path.exists() and str(src_path) not in sys.path:
	sys.path.insert(0, str(src_path))

# Ensure repository root is also present (for web/ and other modules).
if str(repo_root) not in sys.path:
	sys.path.insert(0, str(repo_root))

# Import and execute the Streamlit app implementation
importlib.import_module("web.app")
