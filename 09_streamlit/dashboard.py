"""
Data Science Salaries Dashboard
Built with Streamlit + Pandas + Matplotlib

Uses only things we learned in class:
    - Pandas: read_csv, head, loc, boolean masks, groupby + agg,
      sort_values, apply, lambda
    - Matplotlib: scatter, bar, hist, alpha, colors, title, labels

Run it with:
    streamlit run dashboard.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


# ----------------------------------------------------------------------
# 1. Page setup
# ----------------------------------------------------------------------
st.set_page_config(page_title="Data Science Salaries 2024", layout="wide")

st.title("Data Science Salaries Dashboard")
st.write("Explore salaries of data professionals around the world.")


# ----------------------------------------------------------------------
# 2. Load the data (same way we did in the pandas classes)
# ----------------------------------------------------------------------
df = pd.read_csv("DataScience_salaries_2024.csv")

# Make the experience codes friendlier using apply + lambda (lesson 04).
exp_names = {"EN": "Entry", "MI": "Mid", "SE": "Senior", "EX": "Expert"}
df["experience_name"] = df["experience_level"].apply(lambda x: exp_names[x])


# ----------------------------------------------------------------------
# 3. Sidebar filters
# ----------------------------------------------------------------------
st.sidebar.header("Filters")

exp_levels = st.sidebar.multiselect(
    "Experience level",
    options=["EN", "MI", "SE", "EX"],
    default=["EN", "MI", "SE", "EX"],
    format_func=lambda x: exp_names[x],
)

years = sorted(df["work_year"].unique())
year_range = st.sidebar.select_slider(
    "Work year",
    options=years,
    value=(min(years), max(years)),
)

sizes = st.sidebar.multiselect(
    "Company size",
    options=["S", "M", "L"],
    default=["S", "M", "L"],
)


# ----------------------------------------------------------------------
# 4. Filter the data with a boolean mask (lesson 03)
# ----------------------------------------------------------------------
mask = (
    (df["experience_level"].apply(lambda x: x in exp_levels))
    & (df["work_year"] >= year_range[0])
    & (df["work_year"] <= year_range[1])
    & (df["company_size"].apply(lambda x: x in sizes))
)
data = df.loc[mask]

if len(data) == 0:
    st.warning("No data matches the filters. Try changing them in the sidebar.")
    st.stop()


# ----------------------------------------------------------------------
# 5. Some KPIs at the top
# ----------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Records", len(data))
col2.metric("Avg salary (USD)", f"${data['salary_in_usd'].mean():,.0f}")
col3.metric("Median salary (USD)", f"${data['salary_in_usd'].median():,.0f}")
col4.metric("Countries", data["company_location"].nunique())

st.divider()


# ----------------------------------------------------------------------
# 6. Charts
# ----------------------------------------------------------------------
left, right = st.columns(2)

# --- Chart 1: average salary by experience level (groupby + bar plot) ---
with left:
    st.subheader("Average salary by experience level")

    # groupby + agg("mean") — exactly the pattern from lesson 04
    avg_by_exp = data.groupby("experience_name")[["salary_in_usd"]].agg("mean")

    # sort the bars in a logical order (Entry -> Expert)
    order = ["Entry", "Mid", "Senior", "Expert"]
    avg_by_exp = avg_by_exp.loc[[o for o in order if o in avg_by_exp.index]]

    fig, ax = plt.subplots()
    ax.bar(
        avg_by_exp.index,
        avg_by_exp["salary_in_usd"],
        color=["#5B9BD5", "#70AD47", "#FFC000", "#C00000"],
    )
    ax.set_title("Experience pays off")
    ax.set_xlabel("Experience level")
    ax.set_ylabel("Avg salary (USD)")
    st.pyplot(fig)

# --- Chart 2: salary distribution (histogram) ---
with right:
    st.subheader("Salary distribution")

    bins = st.slider("Number of bins", 10, 80, 30)

    fig, ax = plt.subplots()
    ax.hist(data["salary_in_usd"], bins=bins, color="#5B9BD5", edgecolor="white")
    ax.set_title("How are salaries spread?")
    ax.set_xlabel("Salary (USD)")
    ax.set_ylabel("Count")
    st.pyplot(fig)


# --- Chart 3: scatter plot, salary over the years by experience level ---
st.subheader("Salary over the years")

colors = {"EN": "#5B9BD5", "MI": "#70AD47", "SE": "#FFC000", "EX": "#C00000"}

fig, ax = plt.subplots(figsize=(10, 4))
for level in exp_levels:
    sub = data.loc[data["experience_level"] == level]
    ax.scatter(
        sub["work_year"],
        sub["salary_in_usd"],
        alpha=0.4,
        color=colors[level],
        label=exp_names[level],
    )
ax.set_title("Salary vs. year, by experience level")
ax.set_xlabel("Work year")
ax.set_ylabel("Salary (USD)")
ax.legend()
st.pyplot(fig)


# --- Chart 4: top job titles (groupby + agg + sort_values) ---
st.subheader("Top job titles by average salary")
top_n = st.slider("How many job titles?", 5, 20, 10)

# groupby + agg with mean and count (lesson 04)
job_stats = data.groupby("job_title")[["salary_in_usd"]].agg(["mean", "count"])
job_stats.columns = ["avg_salary", "n"]

# keep only titles with enough data and sort (lesson 03)
job_stats = job_stats.loc[job_stats["n"] >= 5]
job_stats = job_stats.sort_values("avg_salary", ascending=False).head(top_n)

fig, ax = plt.subplots(figsize=(10, 5))
# reverse so the highest salary sits at the top of the chart
ax.barh(job_stats.index[::-1], job_stats["avg_salary"][::-1], color="#70AD47")
ax.set_title(f"Top {top_n} job titles (at least 5 records)")
ax.set_xlabel("Average salary (USD)")
st.pyplot(fig)


# ----------------------------------------------------------------------
# 7. Raw data table
# ----------------------------------------------------------------------
with st.expander("Show raw data"):
    st.dataframe(data.head(200))
    st.write(f"Showing the first 200 rows of {len(data)} total.")
