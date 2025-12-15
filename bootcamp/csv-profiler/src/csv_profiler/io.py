from csv import DictReader
from pathlib import Path

def read_csv(path: str) -> list[dict[str, str]]:
    with Path(path).open(encoding="utf-8") as f:
        return list(DictReader(f))
