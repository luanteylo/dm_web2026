# Streamlit Tutorial

Welcome! In this short tutorial we will learn just enough Streamlit to build a
nice dashboard on top of the Data Science salaries dataset.

Streamlit turns a Python script into a web app. You write a normal `.py` file
with a few `st.` commands, and Streamlit handles the browser, layout and
interactivity for you.

## Setup

Install the library (only once):

```bash
pip install streamlit
```

Run any Streamlit app from the terminal:

```bash
streamlit run dashboard.py
```

Streamlit will open a tab in your browser. Every time you save the file, the
page reloads automatically.

A Streamlit script always starts with:

```python
import streamlit as st
```

The convention is `st`, the same way we use `pd` for pandas and `plt` for
matplotlib.

---

## 1. Page setup and text

The first thing in our script is the page configuration and some text.

```python
st.set_page_config(page_title="Data Science Salaries 2024", layout="wide")

st.title("Data Science Salaries Dashboard")
st.write("Explore salaries of data professionals around the world.")
```

| Command              | What it does                                        |
|----------------------|-----------------------------------------------------|
| `st.set_page_config` | Sets the browser tab title and page layout         |
| `st.title`           | A big title at the top of the page                  |
| `st.write`           | Writes text, numbers, or even DataFrames           |
| `st.subheader`       | A smaller section title (used later)               |
| `st.divider`         | Draws a horizontal line to split sections          |

> Tip: `layout="wide"` makes the page use the full width of the browser, which
> is much nicer for dashboards.

---

## 2. Loading data

Streamlit does not change anything about pandas. We load the CSV like always:

```python
df = pd.read_csv("DataScience_salaries_2024.csv")
```

The interesting part is what we do with the DataFrame afterwards. To display
it on the page, we use:

```python
st.dataframe(df.head(10))
```

`st.dataframe` shows an interactive table the user can scroll and sort.

---

## 3. Widgets (the interactive part)

Widgets are inputs the user can change. The really cool thing in Streamlit is
this: **the widget returns the value the user picked**, and the script re-runs
every time it changes.

```python
n = st.slider("How many rows?", 1, 100, 10)
st.dataframe(df.head(n))
```

The widgets we use in our dashboard:

### `st.multiselect` — pick many items from a list

```python
exp_levels = st.multiselect(
    "Experience level",
    options=["EN", "MI", "SE", "EX"],
    default=["EN", "MI", "SE", "EX"],
)
```

`exp_levels` is a **list** with the items the user selected.

### `st.select_slider` — slider that picks from a fixed list

```python
years = sorted(df["work_year"].unique())
year_range = st.select_slider(
    "Work year",
    options=years,
    value=(min(years), max(years)),
)
```

When `value` is a tuple, the user gets a range slider with two handles.

### `st.slider` — slider over numbers

```python
bins = st.slider("Number of bins", 10, 80, 30)
```

The three numbers mean: minimum, maximum, default.

### Putting widgets in the sidebar

Anything prefixed with `st.sidebar.` shows up in the left sidebar instead of
the main page:

```python
st.sidebar.header("Filters")
exp_levels = st.sidebar.multiselect(...)
```

---

## 4. Filtering with the widget values

Once a widget gives us a value, we use **plain pandas** to filter, exactly
like in lessons 03 and 04:

```python
mask = (
    (df["experience_level"].apply(lambda x: x in exp_levels))
    & (df["work_year"] >= year_range[0])
    & (df["work_year"] <= year_range[1])
)
data = df.loc[mask]
```

If the result is empty, we can stop the script early:

```python
if len(data) == 0:
    st.warning("No data matches the filters.")
    st.stop()
```

| Command       | What it does                                |
|---------------|---------------------------------------------|
| `st.warning`  | Yellow message box                          |
| `st.info`     | Blue message box                            |
| `st.success`  | Green message box                           |
| `st.error`    | Red message box                             |
| `st.stop`     | Stops the script right there                |

---

## 5. Layout: columns

To put things side by side we use `st.columns(n)`:

```python
col1, col2, col3 = st.columns(3)
col1.write("Left")
col2.write("Middle")
col3.write("Right")
```

A nice pattern for KPIs is:

```python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Records", len(data))
col2.metric("Avg salary (USD)", f"${data['salary_in_usd'].mean():,.0f}")
col3.metric("Median salary (USD)", f"${data['salary_in_usd'].median():,.0f}")
col4.metric("Countries", data["company_location"].nunique())
```

`st.metric` shows a big number with a small label on top. Perfect for KPIs.

You can also use columns with a `with` block:

```python
left, right = st.columns(2)
with left:
    st.subheader("Left chart")
    # ... plot here
with right:
    st.subheader("Right chart")
    # ... plot here
```

---

## 6. Showing matplotlib charts

This is the bridge between matplotlib and Streamlit. Make the figure as
usual, then pass it to `st.pyplot`:

```python
fig, ax = plt.subplots()
ax.bar(["A", "B", "C"], [3, 1, 2], color="#5B9BD5")
ax.set_title("My chart")
ax.set_xlabel("x")
ax.set_ylabel("y")

st.pyplot(fig)
```

That's it. Anything we learned in matplotlib classes works: `scatter`, `hist`,
`bar`, `barh`, `alpha`, `color`, `cmap`, `legend`, etc.

---

## 7. Putting widgets and charts together

Because the whole script re-runs on every interaction, you can put a widget
right next to its chart and the chart will update automatically:

```python
bins = st.slider("Number of bins", 10, 80, 30)

fig, ax = plt.subplots()
ax.hist(data["salary_in_usd"], bins=bins, color="#5B9BD5")
ax.set_title("Salary distribution")
st.pyplot(fig)
```

When the user moves the slider, the script re-runs, `bins` gets the new
value, and the histogram is redrawn. That is the whole magic.

---

## 8. Expanders

To hide things that are not the main point (raw data, debug info, etc.):

```python
with st.expander("Show raw data"):
    st.dataframe(data.head(200))
```

The user clicks to open it.

---

## Cheat sheet

| Goal                          | Command                                |
|-------------------------------|----------------------------------------|
| Page configuration            | `st.set_page_config(...)`              |
| Big title                     | `st.title("...")`                      |
| Section title                 | `st.subheader("...")`                  |
| Plain text                    | `st.write("...")`                      |
| Horizontal line               | `st.divider()`                         |
| Show a DataFrame              | `st.dataframe(df)`                     |
| Show a matplotlib figure      | `st.pyplot(fig)`                       |
| Big KPI number                | `st.metric(label, value)`              |
| Side-by-side layout           | `c1, c2 = st.columns(2)`               |
| Sidebar                       | `st.sidebar.<anything>`                |
| Pick one option               | `st.selectbox(label, options)`         |
| Pick many options             | `st.multiselect(label, options)`       |
| Number slider                 | `st.slider(label, min, max, default)`  |
| Slider over a list            | `st.select_slider(label, options=...)` |
| Text input                    | `st.text_input(label)`                 |
| Checkbox                      | `st.checkbox(label)`                   |
| Hide section behind a click   | `with st.expander("..."):`             |
| Stop the script               | `st.stop()`                            |
| Warning / info / error box    | `st.warning / st.info / st.error`      |

---

## How to read this together with the code

Open `dashboard_starter.py` side by side with this tutorial. Each section in
the starter file matches a section here:

1. Page setup -> `st.set_page_config`, `st.title`, `st.write`
2. Load data -> `pd.read_csv` + `apply` + `lambda`
3. Sidebar filters -> `st.sidebar.multiselect`, `st.sidebar.select_slider`
4. Apply the filters -> boolean mask + `df.loc[...]`
5. KPIs -> `st.columns` + `st.metric`
6. Charts -> matplotlib + `st.pyplot`
7. Raw data -> `st.expander` + `st.dataframe`

When you finish the dashboard, the file should look very close to
`dashboard.py`. Have fun!
