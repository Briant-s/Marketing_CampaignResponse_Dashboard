import streamlit as st

st.set_page_config(page_title="Campaign Target Dashboard", layout="wide")

# ========================================================
# SIDEBAR
# ========================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard Overview"

st.sidebar.title("Navigation")

if st.sidebar.button("Home Page", width="stretch", type="primary"):
    st.session_state.current_page = "Home Page"

if st.sidebar.button("Dashboard Overview", width="stretch"):
    st.session_state.current_page = "Dashboard Overview"

if st.sidebar.button("Predict Individual Target", width="stretch"):
    st.session_state.current_page = "Predict Individual Target"

st.sidebar.divider()
st.sidebar.caption("Model Version: v1.0.1")

# Routing Logic
if st.session_state.current_page == "Home Page":
    from views import home
    home.show_page()
elif st.session_state.current_page == "Dashboard Overview":
    from views import dashboard
    dashboard.show_page()
elif st.session_state.current_page == "Predict Individual Target":
    from views import prediction
    prediction.show_page()

