import os
import json
import csv
from datetime import datetime
from typing import List, Dict


def read_file(file_path: str) -> List[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_json(file_path: str, data: List[Dict]):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def write_csv(file_path: str, data: List[Dict]):
    if not data:
        return
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def timestamped_filename(prefix: str, ext: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{ext}"


def chunk_list(data: List, chunk_size: int) -> List[List]:
    return [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]


def safe_get(d: dict, key: str, default=None):
    return d.get(key, default)


def flatten_list(nested_list: List[List]) -> List:
    return [item for sublist in nested_list for item in sublist]


def merge_dicts(dicts: List[Dict]) -> Dict:
    result = {}
    for d in dicts:
        result.update(d)
    return result
