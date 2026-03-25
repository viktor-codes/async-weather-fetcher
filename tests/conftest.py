import sys
from pathlib import Path


# Чтобы `import app...` работал при запуске `pytest` из корня репозитория.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

