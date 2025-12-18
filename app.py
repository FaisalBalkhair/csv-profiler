import csv

import streamlit as st
import csv
from io import StringIO
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown
import json
from pathlib import Path

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")
st.caption("Upload a CSV file to generate a profiling report (JSON + Markdown)")


st.sidebar.header("Inputs")
rows = None
report = st.session_state.get("report")
st.write("Upload a CSV file from the sidebar to get started")
uploaded = st.file_uploader("Upload a CSV file", type=['csv'])
show_preview = st.sidebar.checkbox("Show preview", value=False)

if uploaded is not None:
    text = uploaded.getvalue().decode("utf-8-sig")
    rows = list(csv.DictReader(StringIO(text)))

    if len(rows) == 0:
        st.error("CSV has no data. Upload a CSV with at least 1 row.")
        st.stop()

    if len(rows[0]) == 0:
        st.warning("CSV has no headers (no columns detected).")


    if rows:
        if st.button("Generate report"):
            report = profile_rows(rows)
            st.session_state["report"] = report
            st.success("Report generated successfully!")

    if "report" in st.session_state:
        report = st.session_state["report"]
        st.subheader("Report summary")
        st.write(f"Rows: {report['n_rows']}")
        st.write(f"Columns: {report['n_cols']}")

        st.subheader("Columns overview")
        table_rows = []
        for col in report["columns"]:
            table_rows.append({
                "Column": col["name"],
                "Type": col["type"],
                "Missing": col["missing"],
                "Missing %": f"{col['missing_pct']:.1f}%",
                "Unique": col["unique"],
            })
        st.dataframe(table_rows)
        with st.expander("Markdown preview"):
            st.markdown(render_markdown(report))

        st.subheader("Export")
        report_name = st.text_input("Report name", value="report")
        report = st.session_state["report"]
        json_content = json.dumps(report, indent=2)
        md_content = render_markdown(report)
        st.download_button(
            label="Download JSON",
            data=json_content,
            file_name=f"{report_name}.json",
        )

        st.download_button(
            label="Download Markdown",
            data=md_content,
            file_name=f"{report_name}.md",
        )
        if st.button("Save to outputs"):
            out_dir = Path("outputs")
            out_dir.mkdir(parents=True, exist_ok=True)

            (out_dir / f"{report_name}.json").write_text(json_content, encoding="utf-8")
            (out_dir / f"{report_name}.md").write_text(md_content, encoding="utf-8")

            st.success("Saved report.json and report.md to outputs/")

    if show_preview:
        st.subheader("Preview")
        st.write(rows[:5])
else:
    st.info("Upload a csv to begin")


