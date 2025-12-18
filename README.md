## CSV-Profiler

```markdown
## Setup

uv venv -p 3.11
uv pip install -r pyproject.txt

## Run CLI

# If you have a src/ folder:

# Mac/Linux: export PYTHONPATH=src

# Windows: $env:PYTHONPATH="src"

uv run python -m csv_profiler.cli data/sample.csv --out-dir outputs

## Run GUI

# If you have a src/ folder:

# Mac/Linux: export PYTHONPATH=src

# Windows: $env:PYTHONPATH="src"

uv run streamlit run app.py
```

### Expected output

After running the CLI command, the following files will be created:

```text
outputs/report.json
outputs/report.md
```
