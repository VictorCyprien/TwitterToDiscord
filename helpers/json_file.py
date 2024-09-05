from typing import List, Dict
import json
from json import JSONDecodeError

def open_json(filename: str) -> List[Dict] | Dict:
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
    except JSONDecodeError:
        data = None
    except FileNotFoundError:
        data = None
    return data

def save_json(filename: str, data):
    with open(filename, 'w') as f:
        json.dump(data, f)
