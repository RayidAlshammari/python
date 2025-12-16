from collections import Counter

MISSING_VALUES = {"", "na", "n/a", "null", "none", "nan"}


def is_missing(value) -> bool:

    if value is None:
        return True

    str_value = str(value).strip().lower()

    return str_value in MISSING_VALUES


def try_float(value) -> float | None:

    try:
        return float(value)
    except (ValueError, TypeError):
        return None


def infer_type(values: list) -> str:

    non_missing = [v for v in values if not is_missing(v)]

    if not non_missing:
        return "text"

    for value in non_missing:
        if try_float(value) is None:
            return "text"

    return "number"


def numeric_stats(values: list) -> dict:

    numbers = []
    for value in values:
        if not is_missing(value):
            num = try_float(value)
            if num is not None:
                numbers.append(num)

    missing_count = len(values) - len(numbers)
    unique_count = len(set(numbers)) if numbers else 0

    stats = {
        "count": len(numbers),
        "missing": missing_count,
        "unique": unique_count,
    }

    if numbers:
        stats["min"] = min(numbers)
        stats["max"] = max(numbers)
        stats["mean"] = round(sum(numbers) / len(numbers), 2)
    else:
        stats["min"] = None
        stats["max"] = None
        stats["mean"] = None

    return stats


def text_stats(values: list, top_k: int = 3) -> dict:

    non_missing = [str(v).strip() for v in values if not is_missing(v)]

    missing_count = len(values) - len(non_missing)
    unique_count = len(set(non_missing))

    counter = Counter(non_missing)
    top_values = [
        {"value": value, "count": count}
        for value, count in counter.most_common(top_k)
    ]

    return {
        "count": len(non_missing),
        "missing": missing_count,
        "unique": unique_count,
        "top": top_values,
    }


def profile_csv(rows: list[dict[str, str]]) -> dict:

    if not rows:
        return {
            "n_rows": 0,
            "n_cols": 0,
            "columns": []
        }

    column_names = list(rows[0].keys())

    result = {
        "n_rows": len(rows),
        "n_cols": len(column_names),
        "columns": []
    }

    for col_name in column_names:
        values = [row.get(col_name, "") for row in rows]

        col_type = infer_type(values)

        if col_type == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        column_profile = {
            "name": col_name,
            "type": col_type,
            **stats  
        }

        result["columns"].append(column_profile)

    return result
