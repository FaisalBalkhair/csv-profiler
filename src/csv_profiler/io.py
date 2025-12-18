from __future__ import annotations
from csv import DictReader
from pathlib import Path
import csv

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    with open(p, mode='r', newline='') as file:
        reader = DictReader(file)
        rows = list(reader)
        if not rows:
            raise ValueError(f"CSV file no rows: {p}")
        return rows


