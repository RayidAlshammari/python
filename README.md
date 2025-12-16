# CSV Profiler
**Version:** 1.0.0

**Week 1 Project - SDAIA Academy Bootcamp**

A comprehensive CSV analysis tool that provides statistical profiling with both CLI and GUI interfaces.

## Project Overview

This tool analyzes CSV files and generates detailed statistical reports including data types, missing values, and statistics for both numeric and text columns.

## Project Structure

```
csv-profiler/
├── src/csv_profiler/
│   ├── io.py          # CSV file reading
│   ├── profiling.py   # Core logic (6 functions)
│   ├── render.py      # Output formatting
│   └── cli.py         # CLI interface
├── app.py             # Streamlit GUI
├── data/              # Sample CSV files
└── outputs/           # Generated reports
```

## Data Flow

```
Entry Points:
  - CLI (Typer)      ─┐
  - GUI (Streamlit)  ─┤
                     └──→ [IO → Profiling → Render]
                                           │
                           ┌───────────────┴──────────┐
                           │                          │
                  CLI: Save files         GUI: Display & Download
```

## Core Functions

The project contains 6 core functions in `profiling.py`:

1. **`is_missing(value)`** - Detects missing values (empty, "na", "null", etc.)
2. **`try_float(value)`** - Safely converts values to float
3. **`infer_type(values)`** - Determines column type (number/text)
4. **`numeric_stats(values)`** - Calculates min, max, mean for numeric columns
5. **`text_stats(values)`** - Counts top values for text columns
6. **`profile_csv(rows)`** - Main profiling function that orchestrates the analysis

## Features

- Automatic data type detection (numeric/text)
- Missing value detection with multiple patterns
- Statistical analysis per column type
- Dual interfaces: CLI and Web GUI
- Export formats: JSON and Markdown

## Installation

**One-time setup** - Install the package in development mode:

```bash
cd csv-profiler
pip install -e .
```

This makes the `csv-profiler` command available anywhere on your system!

## Usage

### CLI Commands

```bash
# Basic usage - Simple!
csv-profiler profile data/saudi_shopping_with_missing.csv

# With verbose output (shows summary table)
csv-profiler profile data/saudi_shopping_with_missing.csv --verbose

# Custom output directory and report name
csv-profiler profile data/saudi_shopping_with_missing.csv \
  --out-dir my_reports \
  --report-name analysis
```

**CLI Options:**
- `csv_file` - Path to CSV file (required)
- `--out-dir` / `-o` - Output directory (default: outputs)
- `--report-name` / `-n` - Report name (default: report)
- `--verbose` / `-v` - Display detailed summary table
- `--help` - Show help message

### GUI (Streamlit)

```bash
cd csv-profiler
streamlit run app.py
```

Opens web interface at `http://localhost:8501`

**GUI Features:**
1. Upload CSV file via sidebar
2. Preview first 10 rows
3. Click "Generate Profile" button
4. View results in interactive tables

## Output

**CLI Output:**
- Saves `report.json` and `report.md` to specified output directory
- Optional verbose table displayed in terminal

**GUI Output:**
- Interactive display of profile results
- Downloadable JSON and Markdown reports
- Real-time preview of data

---

**Author:** SDAIA Academy Bootcamp Student : Rayid Alshammari

**Project:** Week 1 Project
