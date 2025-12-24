"""Streamlit app entry point for uvx."""
import sys
import subprocess
from pathlib import Path


def main():
    """Launch Streamlit app."""
    app_path = Path(__file__).parent / "streamlit_app.py"
    sys.exit(subprocess.call(["streamlit", "run", str(app_path)]))


if __name__ == "__main__":
    main()
