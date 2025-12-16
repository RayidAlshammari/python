from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from csv_profiler.io import read_csv
from csv_profiler.profiling import profile_csv
from csv_profiler.render import to_json, to_markdown


app = typer.Typer(help="CSV Profiler - Generate detailed profiles of CSV files")
console = Console()


@app.command()
def profile(
    csv_file: Path = typer.Argument(
        ...,
        help="Path to the CSV file to profile",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
    ),
    out_dir: Optional[Path] = typer.Option(
        "outputs",
        "--out-dir",
        "-o",
        help="Output directory for reports",
    ),
    report_name: Optional[str] = typer.Option(
        "report",
        "--report-name",
        "-n",
        help="Base name for output files (without extension)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed output",
    ),
) -> None:
    
    try:

        console.print(f"\n[bold blue]Reading CSV file:[/bold blue] {csv_file}")
        rows = read_csv(str(csv_file))

        if not rows:
            console.print("[yellow]Warning: CSV file is empty[/yellow]")
            raise typer.Exit(code=1)

        console.print(f"[green]✓[/green] Loaded {len(rows)} rows")


        console.print("\n[bold blue]Profiling data...[/bold blue]")
        profile_data = profile_csv(rows)
        console.print(
            f"[green]✓[/green] Profiled {profile_data['n_cols']} columns"
        )


        if verbose:
            _display_summary(profile_data)


        out_dir.mkdir(parents=True, exist_ok=True)


        json_path = out_dir / f"{report_name}.json"
        console.print(f"\n[bold blue]Writing JSON report:[/bold blue] {json_path}")
        json_content = to_json(profile_data)
        json_path.write_text(json_content, encoding="utf-8")
        console.print(f"[green]✓[/green] JSON report saved")


        md_path = out_dir / f"{report_name}.md"
        console.print(f"[bold blue]Writing Markdown report:[/bold blue] {md_path}")
        md_content = to_markdown(profile_data)
        md_path.write_text(md_content, encoding="utf-8")
        console.print(f"[green]✓[/green] Markdown report saved")


        console.print(
            f"\n[bold green]✓ Profiling complete![/bold green] "
            f"Reports saved to {out_dir}"
        )

    except FileNotFoundError:
        console.print(
            f"[bold red]Error:[/bold red] File not found: {csv_file}",
            style="red",
        )
        raise typer.Exit(code=1)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}", style="red")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=1)


def _display_summary(profile_data: dict) -> None:

    console.print("\n[bold]Profile Summary:[/bold]")


    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Column", style="cyan")
    table.add_column("Type", style="green")
    table.add_column("Count", justify="right")
    table.add_column("Missing", justify="right", style="red")
    table.add_column("Unique", justify="right", style="blue")

    for col in profile_data["columns"]:
        table.add_row(
            col["name"],
            col["type"],
            str(col["count"]),
            str(col["missing"]),
            str(col["unique"]),
        )

    console.print(table)


@app.command()
def version() -> None:
    console.print("[bold]CSV Profiler[/bold] v1.0.0")
    console.print("SDAIA Academy Bootcamp Project")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
