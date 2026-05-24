import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functions.helper import chart_layout, get_theme, get_chart_colors

t = get_theme()
CHART_COLORS = get_chart_colors()

def render_customer(filtered):
    c1, c2 = st.columns(2)
    with c1:
        # Age distribution
        fig = px.histogram(filtered, x="Age", nbins=30)
        chart_layout(fig, "Customer Age Distribution")
        fig.update_traces(marker_line_width=0, opacity=0.85)
        st.plotly_chart(fig, width="content")
    with c2:
        # Income vs Spend scatter
        fig = px.scatter(filtered, x="Income", y="TotalSpend",
                        color="Education", opacity=0.6, size_max=8,
                        hover_data=["Age","Country"])
        chart_layout(fig, "Income vs Total Spend by Education")
        st.plotly_chart(fig, width="content")
    c3, c4 = st.columns(2)
    with c3:
        # Marital status distribution
        ms = filtered["Marital_Status"].value_counts().reset_index()
        ms.columns = ["Status","Count"]
        fig = px.bar(ms, x="Status", y="Count", color="Status")
        chart_layout(fig, "Customers by Marital Status")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
    with c4:
        # Education breakdown donut
        edu = filtered["Education"].value_counts().reset_index()
        edu.columns = ["Education","Count"]
        fig = px.pie(edu, names="Education", values="Count", hole=0.55)
        chart_layout(fig, "Education Level Breakdown")
        fig.update_traces(textposition="outside", textinfo="percent+label")
        st.plotly_chart(fig, width="content")

def render_spending(filtered):
    st.markdown("### Where are customers spending their money?")
 
    spend_cols = {
        "Wines":    "MntWines",
        "Fruits":   "MntFruits",
        "Meat":     "MntMeatProducts",
        "Fish":     "MntFishProducts",
        "Sweets":   "MntSweetProducts",
        "Gold":     "MntGoldProds",
    }
    totals = {k: filtered[v].sum() for k, v in spend_cols.items()}
 
    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(
            x=list(totals.keys()), y=list(totals.values()),
            color=list(totals.keys()),
            labels={"x": "Category", "y": "Total Spend ($)"}
        )
        chart_layout(fig, "Total Spend by Product Category")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    with c2:
        # Channel comparison
        channels = {
            "Deals":    filtered["NumDealsPurchases"].mean(),
            "Web":      filtered["NumWebPurchases"].mean(),
            "Catalog":  filtered["NumCatalogPurchases"].mean(),
            "In-Store": filtered["NumStorePurchases"].mean(),
        }
        fig = px.bar(x=list(channels.keys()), y=list(channels.values()),
                     color=list(channels.keys()),
                     labels={"x":"Channel","y":"Avg Purchases"})
        chart_layout(fig, "Avg Purchases by Channel")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    c3, c4 = st.columns(2)
    with c3:
        # Total spend by age group
        age_spend = filtered.groupby("AgeGroup", observed=True)["TotalSpend"].mean().reset_index()
        fig = px.bar(age_spend, x="AgeGroup", y="TotalSpend",
                     color="AgeGroup",
                     labels={"TotalSpend":"Avg Spend ($)","AgeGroup":"Age Group"})
        chart_layout(fig, "Average Spend by Age Group")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    with c4:
        # Recency vs spend
        fig = px.scatter(filtered, x="Recency", y="TotalSpend",
                         color="AgeGroup", opacity=0.6,
                         labels={"Recency":"Days Since Last Purchase","TotalSpend":"Total Spend"})
        chart_layout(fig, "Recency vs Total Spend")
        st.plotly_chart(fig, width="content")

def render_campaigns(filtered):
    st.markdown("### Which campaigns are working — and for whom?")
 
    cmps = ["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3","AcceptedCmp4","AcceptedCmp5","Response"]
    labels = ["Cmp 1","Cmp 2","Cmp 3","Cmp 4","Cmp 5","Last"]
 
    accept_rates = [filtered[c].mean()*100 for c in cmps]
 
    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure(go.Bar(
            x=labels, y=accept_rates,
            text=[f"{r:.1f}%" for r in accept_rates],
            textposition="outside",
        ))
        chart_layout(fig, "Acceptance Rate per Campaign (%)")
        fig.update_layout(yaxis_range=[0, max(accept_rates)*1.3])
        st.plotly_chart(fig, width="content")
 
    with c2:
        # Campaign acceptance by education
        edu_accept = filtered.groupby("Education")[cmps].mean().reset_index()
        fig = px.bar(edu_accept.melt(id_vars="Education", var_name="Campaign", value_name="Rate"),
                     x="Education", y="Rate", color="Campaign", barmode="group",
                     labels={"Rate":"Acceptance Rate"})
        chart_layout(fig, "Campaign Acceptance by Education Level")
        st.plotly_chart(fig, width="content")
 
    c3, c4 = st.columns(2)
    with c3:
        # Acceptance by income group
        filtered2 = filtered.copy()
        filtered2["IncomeGroup"] = pd.qcut(filtered2["Income"], q=4,
                                            labels=["Q1 Low","Q2","Q3","Q4 High"])
        ig = filtered2.groupby("IncomeGroup", observed=True)["AnyAccepted"].mean().reset_index()
        fig = px.bar(ig, x="IncomeGroup", y="AnyAccepted",
                     color="IncomeGroup",
                     labels={"AnyAccepted":"Acceptance Rate","IncomeGroup":"Income Quartile"})
        chart_layout(fig, "Any Campaign Accepted by Income Quartile")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    with c4:
        # Spend vs campaign response
        fig = px.box(filtered, x="AnyAccepted", y="TotalSpend",
                     color="AnyAccepted", color_discrete_sequence=[t["primary"],t["secondary"]],
                     labels={"AnyAccepted":"Accepted Campaign","TotalSpend":"Total Spend ($)"})
        chart_layout(fig, "Spenders Who Accepted vs Rejected Campaigns")
        fig.update_layout(showlegend=False)
        fig.update_xaxes(ticktext=["No","Yes"], tickvals=[0,1])
        st.plotly_chart(fig, width="content")

def render_geography(filtered):
    st.markdown("### How do customers differ across regions and life stage?")
 
    c1, c2 = st.columns(2)
    with c1:
        ctry = filtered.groupby("Country").agg(
            Customers=("ID","count"),
            AvgSpend=("TotalSpend","mean"),
            AvgIncome=("Income","mean"),
        ).reset_index()
        fig = px.bar(ctry, x="Country", y="Customers",
                     color="AvgSpend", color_continuous_scale=["#E0F7F7","#2BBFBF","#1B2A4A"],
                     text="Customers",
                     labels={"AvgSpend":"Avg Spend ($)"})
        chart_layout(fig, "Customers per Country (Color = Avg Spend)")
        fig.update_traces(textposition="outside")
        st.plotly_chart(fig, width="content")
 
    with c2:
        fig = px.bar(ctry, x="Country", y="AvgIncome",
                     color="Country", color_discrete_sequence=CHART_COLORS,
                     labels={"AvgIncome":"Average Income ($)"})
        chart_layout(fig, "Average Income by Country")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    c3, c4 = st.columns(2)
    with c3:
        # Kids + Teens at home vs spend
        filtered["Children"] = filtered["Kidhome"] + filtered["Teenhome"]
        ch_spend = filtered.groupby("Children")["TotalSpend"].mean().reset_index()
        fig = px.bar(ch_spend, x="Children", y="TotalSpend",
                     color="Children", color_discrete_sequence=CHART_COLORS,
                     labels={"TotalSpend":"Avg Total Spend ($)","Children":"Children at Home"})
        chart_layout(fig, "Avg Spend by Number of Children at Home")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, width="content")
 
    with c4:
        # Web visits vs web purchases
        fig = px.scatter(filtered, x="NumWebVisitsMonth", y="NumWebPurchases",
                         color="Education", opacity=0.55,
                         color_discrete_sequence=CHART_COLORS,
                         trendline="ols",
                         trendline_color_override=t["secondary"],
                         labels={"NumWebVisitsMonth":"Monthly Web Visits",
                                 "NumWebPurchases":"Web Purchases"})
        chart_layout(fig, "Web Visits vs Web Purchases (with trend)")
        st.plotly_chart(fig, width="content")