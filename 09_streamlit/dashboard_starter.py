"""
Data Science Salaries Dashboard - STARTER FILE
We will build this together in class.

Run it with:
    streamlit run dashboard_starter.py

Dataset columns:
    work_year, experience_level, employment_type, job_title,
    salary, salary_currency, salary_in_usd, employee_residence,
    remote_ratio, company_location, company_size

experience_level: EN (Entry), MI (Mid), SE (Senior), EX (Expert)
company_size:     S (Small), M (Medium), L (Large)
remote_ratio:     0 (on-site), 50 (hybrid), 100 (fully remote)

We will use ONLY things we already know:
    - Pandas: read_csv, head, loc, boolean masks, groupby + agg,
      sort_values, apply, lambda
    - Matplotlib: scatter, bar, hist, alpha, colors, title, labels
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ----------------------------------------------------------------------
# 1. Page setup
# ----------------------------------------------------------------------
# TODO: use st.set_page_config to set a page_title and layout="wide"
# TODO: add a title with st.title and a short intro with st.write


# ----------------------------------------------------------------------
# 2. Load the data (just like in the pandas classes)
# ----------------------------------------------------------------------
# TODO: read "DataScience_salaries_2024.csv" into a DataFrame `df`

# TODO: using apply + lambda, create a new column "experience_name"
#       that maps EN -> "Entry", MI -> "Mid", SE -> "Senior", EX -> "Expert"
# exp_names = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Expert"}


# ----------------------------------------------------------------------
# 3. Sidebar filters
# ----------------------------------------------------------------------
# st.sidebar.header("Filters")

# TODO: a multiselect for experience_level (EN, MI, SE, EX)
# TODO: a select_slider for the year range
# TODO: a multiselect for company_size (S, M, L)


# ----------------------------------------------------------------------
# 4. Apply the filters with a boolean mask (lesson 03)
# ----------------------------------------------------------------------
# Example of a boolean mask:
#     mask = (df["work_year"] >= 2021) & (df["work_year"] <= 2023)
#     data = df.loc[mask]
#
# TODO: build the mask combining all three filters and create `data`

# TODO: if the data is empty, show a warning and call st.stop()


# ----------------------------------------------------------------------
# 5. KPIs at the top (st.columns + st.metric)
# ----------------------------------------------------------------------
# TODO: show 4 metrics:
#   - number of records          -> len(data)
#   - average salary in USD      -> data["salary_in_usd"].mean()
#   - median salary in USD       -> data["salary_in_usd"].median()
#   - number of unique countries -> data["company_location"].nunique()


# ----------------------------------------------------------------------
# 6. Charts
# ----------------------------------------------------------------------

# --- Chart 1: bar chart of average salary by experience level ---
# TIP: use groupby("experience_name")[["salary_in_usd"]].agg("mean")
# TODO: create a matplotlib figure with ax.bar(...) and show it with st.pyplot(fig)


# --- Chart 2: histogram of salary_in_usd ---
# TODO: add an st.slider for the number of bins
# TODO: build a histogram with ax.hist(...) and show it


# --- Chart 3: scatter plot of salary over the years ---
# TIP: loop over the experience levels and plot one scatter per level
# colors = {"EN": "#5B9BD5", "MI": "#70AD47", "SE": "#FFC000", "EX": "#C00000"}
# TODO: for each level, filter with data.loc[...] and plot ax.scatter(...)
#       with alpha=0.4 because the points overlap a lot
# TODO: add a legend, title and axis labels


# --- Chart 4: top N job titles by average salary ---
# TIP: groupby("job_title")[["salary_in_usd"]].agg(["mean", "count"])
#      keep only titles with at least 5 records
#      sort_values + head(top_n)
# TODO: add a slider for top_n
# TODO: plot a horizontal bar chart with ax.barh(...)


# ----------------------------------------------------------------------
# 7. Show the filtered data
# ----------------------------------------------------------------------
# TODO: inside an st.expander, display data.head(200) with st.dataframe
