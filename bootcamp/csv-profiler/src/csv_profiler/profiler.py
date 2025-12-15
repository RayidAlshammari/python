def profile(rows: list[dict[str, str]]) -> dict:
    if not rows:
        return {"rows": 0, "columns": {}}

    columns = rows[0].keys()
    report: dict[str, dict] = {"rows": len(rows), "columns": {}}

    for col in columns:
        values = [
            row.get(col, "").strip()
            for row in rows
        ]

        missing = sum(v == "" for v in values)
        non_empty = len(values) - missing

        report["columns"][col] = {
            "missing": missing,
            "non_empty": non_empty,
            "total": len(values),
        }

    return report
