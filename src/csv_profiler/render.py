import json


def to_json(profile: dict) -> str:
    
    
    return json.dumps(profile, indent=2, ensure_ascii=False)


def to_markdown(profile: dict) -> str:

    lines = [
        "# CSV Profiling Report",
        "",
        "## Summary",
        f"- **Rows**: {profile['n_rows']}",
        f"- **Columns**: {profile['n_cols']}",
        "",
        "## Column Details",
        ""
    ]


    lines.append("| Column | Type | Count | Missing | Unique |")
    lines.append("|--------|------|-------|---------|--------|")

    for col in profile["columns"]:
        lines.append(
            f"| {col['name']} | {col['type']} | {col['count']} | "
            f"{col['missing']} | {col['unique']} |"
        )

    lines.append("")


    for col in profile["columns"]:
        lines.append(f"### {col['name']}")
        lines.append("")
        lines.append(f"- **Type**: {col['type']}")
        lines.append(f"- **Count**: {col['count']}")
        lines.append(f"- **Missing**: {col['missing']}")
        lines.append(f"- **Unique**: {col['unique']}")

        if col["type"] == "number":

            lines.append(f"- **Min**: {col.get('min', 'N/A')}")
            lines.append(f"- **Max**: {col.get('max', 'N/A')}")
            lines.append(f"- **Mean**: {col.get('mean', 'N/A')}")
        else:

            lines.append("- **Top Values**:")
            if col.get("top"):
                for item in col["top"]:
                    lines.append(f"  - {item['value']}: {item['count']}")
            else:
                lines.append("  - None")

        lines.append("")

    return "\n".join(lines)
