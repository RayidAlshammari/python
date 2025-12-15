import json
from pathlib import Path

def write_json(report: dict, path: str) -> None:
    Path(path).parent.mkdir(exist_ok=True)
    Path(path).write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def write_md(report: dict, path: str) -> None:
    lines = [f"# CSV Profile\n\nRows: {report['rows']}\n"]

    for col, stats in report["columns"].items():
        lines.extend([
            f"## {col}",
            f"- Missing: {stats['missing']}",
            f"- Non-empty: {stats['non_empty']}",
            f"- Total: {stats['total']}\n",
        ])

    Path(path).write_text("\n".join(lines), encoding="utf-8")
