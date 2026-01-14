import json
from pathlib import Path

def load_test_data(relative_path):
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / relative_path

    with open(file_path, encoding="utf-8") as f:
        return json.load(f)

