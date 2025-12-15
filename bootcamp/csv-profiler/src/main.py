from csv_profiler.io import read_csv
from csv_profiler.profiler import profile
from csv_profiler.render import write_json, write_md

def main() -> None:
    rows = read_csv("data/saudi_shopping_with_missing.csv")
    report = profile(rows)

    write_json(report, "outputs/report.json")
    write_md(report, "outputs/report.md")

if __name__ == "__main__":
    main()
