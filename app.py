import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="STAR98 Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
)

@st.cache_data
def load_data():
    df = pd.read_csv("data/star98_student_performance.csv")
    return df

df = load_data()

st.title("🎓 STAR98 Student Performance Dashboard")
st.caption("Real public education dataset: California STAR 1998 sample via statsmodels. Built for beginner-friendly data analytics portfolio use.")

with st.sidebar:
    st.header("Filters")
    bands = st.multiselect(
        "Performance band",
        sorted(df["performance_band"].unique()),
        default=sorted(df["performance_band"].unique()),
    )
    lowinc_range = st.slider(
        "Low-income students (%)",
        float(df["LOWINC"].min()),
        float(df["LOWINC"].max()),
        (float(df["LOWINC"].min()), float(df["LOWINC"].max())),
    )
    min_tested = st.slider(
        "Minimum students tested",
        int(df["total_tested"].min()),
        int(df["total_tested"].max()),
        int(df["total_tested"].min()),
    )

filtered = df[
    (df["performance_band"].isin(bands))
    & (df["LOWINC"].between(lowinc_range[0], lowinc_range[1]))
    & (df["total_tested"] >= min_tested)
]

k1, k2, k3, k4 = st.columns(4)
k1.metric("Districts", f"{len(filtered):,}")
k2.metric("Avg % Above Math Median", f"{filtered['pct_above_math_median'].mean():.1f}%")
k3.metric("Avg Low-Income %", f"{filtered['LOWINC'].mean():.1f}%")
k4.metric("Total Students Tested", f"{int(filtered['total_tested'].sum()):,}")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Performance distribution")
    fig = px.histogram(
        filtered,
        x="pct_above_math_median",
        color="performance_band",
        nbins=25,
        labels={"pct_above_math_median": "% above national math median"},
        title="District performance distribution",
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Low income vs performance")
    fig = px.scatter(
        filtered,
        x="LOWINC",
        y="pct_above_math_median",
        size="total_tested",
        color="performance_band",
        hover_name="district_id",
        labels={
            "LOWINC": "Low-income students (%)",
            "pct_above_math_median": "% above national math median",
            "total_tested": "Students tested",
        },
        title="Relationship between low-income percentage and math performance",
    )
    st.plotly_chart(fig, use_container_width=True)

left2, right2 = st.columns(2)

with left2:
    st.subheader("Performance by band")
    band_summary = filtered.groupby("performance_band", as_index=False).agg(
        districts=("district_id", "count"),
        avg_above=("pct_above_math_median", "mean"),
        avg_lowinc=("LOWINC", "mean"),
    )
    fig = px.bar(
        band_summary,
        x="performance_band",
        y="districts",
        text="districts",
        title="Number of districts by performance band",
    )
    st.plotly_chart(fig, use_container_width=True)

with right2:
    st.subheader("Prep-course participation")
    fig = px.scatter(
        filtered,
        x="PCTAF",
        y="pct_above_math_median",
        color="performance_band",
        size="total_tested",
        hover_name="district_id",
        labels={
            "PCTAF": "Students taking UC/CSU prep courses (%)",
            "pct_above_math_median": "% above national math median",
        },
        title="Prep-course participation vs math performance",
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Top districts by math performance")
top_n = st.slider("Show top N rows", 5, 30, 10)
st.dataframe(
    filtered.sort_values("pct_above_math_median", ascending=False)[
        [
            "district_id",
            "performance_band",
            "pct_above_math_median",
            "total_tested",
            "LOWINC",
            "PCTAF",
            "PTRATIO",
            "PERSPENK",
        ]
    ].head(top_n),
    use_container_width=True,
)

st.subheader("Full filtered data")
st.dataframe(filtered, use_container_width=True)

st.download_button(
    "Download filtered CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    "filtered_star98_student_performance.csv",
    "text/csv",
)

st.info(
    "Source: statsmodels Star98 Educational Dataset. It is a subset of California STAR 1998 education policy/outcomes data."
)
