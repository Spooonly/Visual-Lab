import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"

def load_reagents():
    path = DATA_DIR / "reagents.json"
    return json.loads(path.read_text(encoding="utf-8"))