"""Expose this standalone script directory under the paper's importlib gate."""

from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent))
