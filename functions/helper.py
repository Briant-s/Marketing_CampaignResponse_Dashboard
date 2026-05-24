import streamlit as st

def get_theme():
    return {
        "primary":    st.get_option("theme.primaryColor"),
        "bg":         st.get_option("theme.backgroundColor"),
        "secondary":  st.get_option("theme.secondaryBackgroundColor"),
        "text":       st.get_option("theme.textColor"),
    }

def chart_layout(fig, title=""):
    t = get_theme()

    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color=t["primary"], family="sans-serif")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="sans-serif", color=t["text"], size=12),
        height=300,
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11),
        colorway=[t["primary"], "#378ADD", "#BA7517", "#639922", "#D85A30"],
    )
    fig.update_xaxes(showgrid=False, showline=True, linecolor=t["secondary"])
    fig.update_yaxes(showgrid=True, gridcolor=t["secondary"], showline=False)
    return fig

def get_chart_colors():
    t = get_theme()
    return [
        t["primary"],           
        "#378ADD",              
        "#BA7517",              
        "#639922",              
        "#D85A30",              
        "#888780",              
    ]