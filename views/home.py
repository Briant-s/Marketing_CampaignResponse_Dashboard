import streamlit as st
from functions.loader import load_data

df = load_data()

def show_page():
    st.title("Campaign Target Dashboard")
    st.caption("Group #8 DA · Model Version v1.0.1")

    st.divider()

    # ── Key dataset stats ────────────────────────────────────────────────
    total_customers  = len(df)
    response_rate    = df["Response"].mean() * 100
    avg_spend        = df["TotalSpend"].mean()
    avg_income       = df["Income"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Customers",  f"{total_customers:,}")
    c2.metric("Response Rate",    f"{response_rate:.1f}%")
    c3.metric("Avg. Total Spend", f"${avg_spend:,.0f}")
    c4.metric("Avg. Income",      f"${avg_income:,.0f}")

    st.divider()

    # ── App guide ────────────────────────────────────────────────────────
    st.subheader("What's inside")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Dashboard Overview**\n\nExplore customer demographics, spending behaviour, campaign performance, and geography. Use the sidebar filters to slice by country, education, and income.")

    with col2:
        st.success("**Spending & Campaigns**\n\nBreak down product spend across categories and compare acceptance rates across all 5 campaign waves.")

    with col3:
        st.warning("**Predict Individual Target**\n\nEnter a customer's profile and get an instant probability score on whether they are likely to respond to a campaign.")

    st.divider()

    # ── Dataset snapshot ─────────────────────────────────────────────────
    st.subheader("Dataset snapshot")
    st.dataframe(
        df.head(10),
        width="content",
        hide_index=True
    )