from __future__ import annotations
from pathlib import Path
import json
from datetime import datetime

def write_json(report:dict, path: str | Path) ->None:

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, mode='w') as f:
        f.write(json.dumps(report, indent=2))

def write_markdown(report:dict, path: str | Path) ->None:

    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    rows = report['summary']['rows']
    columns = report['summary']['columns_count']

    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{rows}**")
    lines.append(f"- Columns: **{columns}**")
    lines.append("")

    lines.append("| Column | Type |  Missing % | Unique |")
    lines.append("|--------|---------|---------|---------|")
    for key, value in report['columns'].items():
        col_type = value['type']
        stats = value['stats']
        missing = stats['missing']
        unique = stats['unique']
        missing_pct = (missing/rows) if rows else 0

        lines.append(f"| {key} | {col_type} | {missing_pct:.1%} | {unique} |")

    for key, value in report["columns"].items():
        col_type = value["type"]
        stats = value["stats"]
        lines.append(f"\n## Column: {key}")
        lines.append(f"- Type: {col_type}")
        lines.append(f"- Missing: {stats['missing']}")
        lines.append(f"- Unique: {stats['unique']}")

        if col_type == "number":
            lines.append(f"- Min: {stats['min']}")
            lines.append(f"- Max: {stats['max']}")
            lines.append(f"- Mean: {stats['mean']}")
        else:
            lines.append("- Top values:")
            for items in stats['top']:
                lines.append(f"  - {items['value']}({items['count']})")

    content = '\n'.join(lines)
    with open(p, mode='w') as f:
        f.write(content)



def render_markdown(report: dict) -> str:
    lines : list[str] = []

    lines.append("# CSV Profiling Report")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")
    lines.append("")

    lines.append("## Dataset summary:")
    lines.append(f"- Rows: **{report.get('n_rows', 0)}**")
    lines.append(f"- Columns: **{report.get('n_cols', 0)}**")
    lines.append("")

    lines.append("## Columns")
    lines.append("")
    lines.append("| Name | Type | Missing | Missing % | Unique |")
    lines.append("|------|------|---------|-----------|--------|")

    for col in report.get("columns", []):
        lines.append(
            f"| {col.get('name')} | {col.get('type')} | "
            f"{col.get('missing')} | "
            f"{col.get('missing_pct', 0):.1f}% | "
            f"{col.get('unique')} |"
        )

    return "\n".join(lines)


