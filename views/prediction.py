import streamlit as st
from pipeline import load_objects, predicts_probs

education_options = ["Basic", "Bachelor", "Master", "PhD"]
marital_options = ["Single", "Married", "Divorced", "Together", "Widow"]


def show_page():
    st.set_page_config(page_title='Campaign Response Predictor', layout='wide')

    @st.cache_resource
    def load():
        return load_objects()

    model, scaler, encoder, cap_bounds, feature_cols, artifacts = load()

    st.title("Campaign Response Predictor")
    st.markdown(
        ":blue-badge[Logistic Regression] :gray-badge[trained on 2.240 Customers]"
    )
        
    st.markdown(
        ":violet-badge[:material/star: 88% Accuracy] :green-badge[Base Response Rate: 15.0%]"
    )
    
    left, right = st.columns(2)
    
    with left:
        with st.container(border=True):
            st.caption("Demographic")
            st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")
            year_birth = st.slider("Birth Year", 1940, 1999, 1975)
            income = st.slider("Annual Income $", 2, 52, 120, format="%dk")
            income = income * 1000
            education     = st.segmented_control("Education", education_options, selection_mode="single")
            marital       = st.segmented_control("Marital Status", marital_options, selection_mode="single")
            kidhome       = st.number_input("Kids at Home", 0, 3, 0)
            teenhome      = st.number_input("Teens at Home", 0, 3, 0)
            st.caption("Engagement")
            st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")

            
            st.caption("Spending (Last 2 Years, $)")
            st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")

            st.caption("Past Campaigns")
            st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")
            accepted_cmp1 = int(st.toggle("Accepted Campaign 1 Offer"))
            accepted_cmp2 = int(st.toggle("Accepted Campaign 2 Offer"))
            accepted_cmp3 = int(st.toggle("Accepted Campaign 3 Offer"))
            accepted_cmp4 = int(st.toggle("Accepted Campaign 4 Offer"))
            accepted_cmp5 = int(st.toggle("Accepted Campaign 5 Offer"))
        
    
    with right:
        st.caption("Response Probability")
        st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")