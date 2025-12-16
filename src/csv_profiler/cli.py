"""Simple CLI for CSV Profiler."""

from pathlib import Path
from typing import Optional
import typer
from rich.console import Console
from rich.table import Table
from csv_profiler.io import read_csv
from csv_profiler.profiling import profile_csv
from csv_profiler.render import to_json, to_markdown

app = typer.Typer(help="📊 CSV Profiler - Analyze your CSV files")
console = Console()


@app.command()
def profile(
    csv_file: Path = typer.Argument(..., help="CSV file to analyze"),
    output: Optional[Path] = typer.Option("outputs", "-o", "--output", help="Output directory"),
    name: Optional[str] = typer.Option("report", "-n", "--name", help="Report name"),
    show: bool = typer.Option(False, "-s", "--show", help="Show results in terminal"),
):
    try:
        # Read CSV
        console.print(f"\n📂 Reading: [cyan]{csv_file}[/cyan]")
        rows = read_csv(str(csv_file))

        if not rows:
            console.print("[yellow]⚠ File is empty[/yellow]")
            raise typer.Exit(1)

        console.print(f"✓ Loaded [green]{len(rows)}[/green] rows")

        # Profile
        console.print("🔍 Analyzing data...")
        profile_data = profile_csv(rows)
        console.print(f"✓ Analyzed [green]{profile_data['n_cols']}[/green] columns")

        # Display summary
        if show:
            console.print("\n[bold]📊 Summary:[/bold]")
            console.print(f"Rows: {profile_data['n_rows']} | Columns: {profile_data['n_cols']}")

            table = Table(show_header=True, header_style="bold cyan")
            table.add_column("Column", style="white")
            table.add_column("Type", style="green")
            table.add_column("Count", justify="right")
            table.add_column("Missing", justify="right", style="yellow")
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

        # Save reports
        output.mkdir(parents=True, exist_ok=True)

        json_path = output / f"{name}.json"
        console.print(f"\n💾 Saving JSON: [cyan]{json_path}[/cyan]")
        json_path.write_text(to_json(profile_data), encoding="utf-8")
        console.print("✓ JSON saved")

        md_path = output / f"{name}.md"
        console.print(f"💾 Saving Markdown: [cyan]{md_path}[/cyan]")
        md_path.write_text(to_markdown(profile_data), encoding="utf-8")
        console.print("✓ Markdown saved")

        console.print(f"\n[bold green]✅ Done![/bold green] Reports in: {output}")

    except FileNotFoundError:
        console.print(f"[bold red]❌ File not found:[/bold red] {csv_file}")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[bold red]❌ Error:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def version():
    console.print("[bold cyan]CSV Profiler[/bold cyan] v1.0.0")
    console.print("SDAIA Academy Bootcamp Project")


def main():
    app()


if __name__ == "__main__":
    main()
