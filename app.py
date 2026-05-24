import streamlit as st
import pandas as pd
from views import customer_overview, home, prediction
from functions.sidefilters import render_filters

st.set_page_config(page_title="Campaign Target Dashboard", layout="wide")


# ========================================================
# SIDEBAR
# ========================================================

with st.sidebar:
    st.header("#8 Data Analytics Team")
    render_filters()
    st.divider()
    st.caption("Prediction Model Version: v1.0.1")
    

# ========================================================
# PAGES
# ========================================================
pages = [
    st.Page(home.show_page, title="Home Page", icon=":material/home:", url_path="home"),
    st.Page(customer_overview.show_page,  title="Customer Overview", icon=":material/overview:", url_path="dashboard"),
    st.Page(prediction.show_page, title="Predict Individual Target", icon=":material/person:", url_path="prediction"),
]

page = st.navigation(pages)


# ========================================================
# RUN — always last
# ========================================================
page.run()