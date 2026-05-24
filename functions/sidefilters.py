import streamlit as st
from functions.loader import load_data  # import your dataframe

df = load_data()

def render_filters():
    # Initialize defaults once
    if "countries" not in st.session_state:
        st.session_state.countries = sorted(df["Country"].dropna().unique().tolist())
    if "edu_levels" not in st.session_state:
        st.session_state.edu_levels = sorted(df["Education"].dropna().unique().tolist())
    if "income_range" not in st.session_state:
        st.session_state.income_range = (int(df["Income"].min()), int(df["Income"].max()))

    with st.sidebar:
        st.subheader("Filters")
        st.multiselect(
            "Country",
            options=sorted(df["Country"].dropna().unique().tolist()),
            key="countries"
        )
        st.multiselect(
            "Education",
            options=sorted(df["Education"].dropna().unique().tolist()),
            key="edu_levels"
        )
        st.slider(
            "Income Range ($)",
            min_value=int(df["Income"].min()),
            max_value=int(df["Income"].max()),
            key="income_range"
        )
    if st.button("↺ Refresh data"):
        st.cache_data.clear()
        st.cache_resource.clear()
        # Reset filters so they reinitialize from fresh df
        for key in ["countries", "edu_levels", "income_range"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()