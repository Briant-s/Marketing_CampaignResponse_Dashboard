# import streamlit as st

# st.set_page_config(page_title="Campaign Target Dashboard", layout="wide")

# # ========================================================
# # SIDEBAR
# # ========================================================
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Dashboard Overview"

# st.sidebar.header("Group #8 DA", divider="gray")

# st.sidebar.caption("Navigation")

# if st.sidebar.button("Home Page", width="stretch", type="primary", icon=":material/home:"):
#     st.session_state.current_page = "Home Page"

# if st.sidebar.button("Dashboard Overview", width="stretch", icon=":material/overview:"):
#     st.session_state.current_page = "Dashboard Overview"

# if st.sidebar.button("Predict Individual Target", width="stretch"):
#     st.session_state.current_page = "Predict Individual Target"

# st.sidebar.divider()
# st.sidebar.caption("Model Version: v1.0.1")

# # Routing Logic
# if st.session_state.current_page == "Home Page":
#     from views import home
#     home.show_page()
# elif st.session_state.current_page == "Dashboard Overview":
#     from views import dashboard
#     dashboard.show_page()
# elif st.session_state.current_page == "Predict Individual Target":
#     from views import prediction
#     prediction.show_page()

import streamlit as st
from views import home, dashboard, prediction

st.set_page_config(page_title="Campaign Target Dashboard", layout="wide")

# ========================================================
# PAGES
# ========================================================
pages = [
    st.Page(home.show_page,       title="Home Page",               icon=":material/home:", url_path="home"),
    st.Page(dashboard.show_page,  title="Dashboard Overview",       icon=":material/overview:", url_path="dashboard"),
    st.Page(prediction.show_page, title="Predict Individual Target", icon=":material/person:", url_path="prediction"),
]

page = st.navigation(pages)

# ========================================================
# SIDEBAR
# ========================================================

st.sidebar.header("Group #8 DA")
st.sidebar.divider()
st.sidebar.caption("Model Version: v1.0.1")


# ========================================================
# RUN — always last
# ========================================================
page.run()

