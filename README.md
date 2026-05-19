# STAR98 Student Performance Dashboard

A GitHub-ready beginner data analytics project using a real public education dataset.

## Dataset

This project uses the **Star98 Educational Dataset** available through `statsmodels`.
It is a subset of California STAR 1998 education policy/outcomes data. The dataset contains 303 district-level/case records and variables such as:

- students above/below the national median in math
- low-income student percentage
- demographic percentage variables
- teacher experience and salary variables
- pupil-teacher ratio
- per-pupil spending
- UC/CSU prep-course participation

A cleaned CSV is included here:

```text
data/star98_student_performance.csv
```

A data dictionary is included here:

```text
data/data_dictionary.csv
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Project structure

```text
star98_student_dashboard/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── star98_student_performance.csv
    └── data_dictionary.csv
```

## Dashboard features

- KPI cards for districts, average performance, low-income percentage, and total tested students
- interactive filters for performance band, low-income range, and minimum tested students
- histogram of math performance
- scatter plots showing relationships between performance and low-income percentage / prep-course participation
- top-performing districts table
- filtered CSV download button

## Source credit

- statsmodels Star98 Educational Dataset documentation: https://www.statsmodels.org/stable/datasets/generated/star98.html

