import json
from pathlib import Path

def load_test_data(filename="login_errors.json"):
    # Assuming the JSON file is in the same folder as this script
    file_path = Path(__file__).parent / filename
    
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)