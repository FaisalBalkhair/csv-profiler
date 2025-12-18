from csv_profiler.io import read_csv_rows
from csv_profiler.profile import basic_profile
from csv_profiler.render import (write_json , write_markdown)
from csv_profiler.strings import slugify
from csv_profiler.profiling import profile_rows



def main() -> None:
    rows = read_csv_rows("data/sample.csv")
    report = profile_rows(rows)

    print(report)
    report = basic_profile(rows)
    write_json(report, "outputs/reports.json")
    write_markdown(report, "outputs/reports.md")
    print("Wrote outputs/report.json and outputs/report.md")
    print(slugify("My Report 01"))

if __name__ == "__main__":
    main()



rows = [{'name' : 'Faisal' , 'Age' : 23},
        {'name' : 'Abduallah' , 'Age' : 24}
        ]

