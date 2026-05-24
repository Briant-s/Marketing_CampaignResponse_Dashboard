#🏠 Overview — Who are our customers and how much are they worth?
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from functions.loader import load_data
from functions.helper import chart_layout, get_theme
from visualizations.viz import *

df = load_data()

def show_page():
    t = get_theme()
    st.title("Customer Overview Demographic")
    filtered = df[
    df["Country"].isin(st.session_state.countries) &
    df["Education"].isin(st.session_state.edu_levels) &
    df["Income"].between(*st.session_state.income_range)
    ]
    # KEY METRICS
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Total Customers",  f"{len(filtered):,}")
    k2.metric("Avg. Income",      f"${filtered['Income'].mean():,.0f}")
    k3.metric("Avg. Total Spend", f"${filtered['TotalSpend'].mean():,.0f}")
    k4.metric("Campaign Accept %",f"{filtered['AnyAccepted'].mean()*100:.1f}%")
    k5.metric("Complaint Rate",   f"{filtered['Complain'].mean()*100:.2f}%")
    tab1, tab2, tab3, tab4 = st.tabs([
        "👤 Demographics",
        "💰 Spending & Products",
        "📢 Campaign Performance",
        "🌍 Geography"
    ])

    with tab1:
        render_customer(filtered)

    with tab2:
        render_spending(filtered)

    with tab3:
        render_campaigns(filtered)

    with tab4:
        render_geography(filtered)


