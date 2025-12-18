from __future__ import annotations
import json
from pathlib import Path
import typer
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown
import time

app = typer.Typer()


@app.command()
def profile(
    csv_path: Path,
    out_dir: Path = Path("outputs"),
    report_name: str = "report",
) -> None:

    start = time.perf_counter()

    out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_csv_rows(csv_path)
    report = profile_rows(rows)

    end = time.perf_counter()
    report["timing_ms"] = round((end - start) * 1000, 2)

    json_path = out_dir / f"{report_name}.json"
    json_path.write_text(
        json.dumps(report, indent=2),
    )

    md_path = out_dir / f"{report_name}.md"
    md_content = render_markdown(report)
    md_path.write_text(md_content)

    typer.echo(f"Wrote {json_path} and {md_path}")


if __name__ == "__main__":
    app()