"""Put this experiment's `drivers` package on the path for its own tests.

`research/` is not a package and `pyproject.toml` does not list these tests in
`testpaths`, so nothing here enters the library suite by accident.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
