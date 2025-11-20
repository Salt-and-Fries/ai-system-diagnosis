import sys
from pathlib import Path

# Ensure the src directory is on the import path for tests
ROOT = Path(__file__).resolve().parents[1]
if ROOT.as_posix() not in sys.path:
    sys.path.insert(0, ROOT.as_posix())
