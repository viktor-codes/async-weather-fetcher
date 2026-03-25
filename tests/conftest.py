import sys
from pathlib import Path


# So `import app...` works when running `pytest` from the repo root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

