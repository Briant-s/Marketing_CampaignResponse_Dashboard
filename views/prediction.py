import streamlit as st
from pipeline import load_objects, predicts_probs
import plotly.graph_objects as go
import pandas as pd
from functions.loader import load_objects

education_options = ["Basic", "Bachelor", "Master", "PhD"]
marital_options = ["Single", "Married", "Divorced", "Together", "Widow"]
std_categories = ["Low", "Medium", "High"]
val_map = {
    "visits": {"Low": 3, "Medium": 10, "High": 17},
    "web":    {"Low": 4, "Medium": 14, "High": 23},
    "cat":    {"Low": 4, "Medium": 14, "High": 24},
    "store":  {"Low": 2, "Medium": 7,  "High": 11},
    "deals":  {"Low": 2, "Medium": 8,  "High": 13}
}

def show_page():
    st.set_page_config(page_title='Campaign Response Predictor', layout='wide')


    model, scaler, encoder, cap_bounds, feature_cols, artifacts = load_objects()

    st.title("Campaign Response Predictor")
    st.markdown(
        ":blue-badge[Logistic Regression] :gray-badge[trained on 2.240 Customers] :violet-badge[:material/star: 88% Accuracy] :green-badge[Base Response Rate: 15.0%]"
    )
        
    
    left, right = st.columns(2)
    
    with right:
        with st.container(border=True):
            st.header("Demographic", divider="gray")
            year_birth = st.slider("Birth Year", 1940, 1999, 1975)
            income = st.slider("Annual Income $", 2, 52, 120, format="%dk")
            income = income * 1000
            col1, col2 = st.columns(2)
            with col1:
                education     = st.segmented_control("Education", education_options, selection_mode="single", default="Bachelor")
            with col2:
                marital       = st.segmented_control("Marital Status", marital_options, selection_mode="single", default="Married")
            col1, col2 = st.columns(2)
            with col1:
                kidhome       = st.number_input("Kids at Home", 0, 3, 0)
            with col2:
                teenhome      = st.number_input("Teens at Home", 0, 3, 0)
            st.header("Engagement", divider="gray")
            col1, col2 = st.columns(2)
            with col1:    
                visit_choice       = st.segmented_control("Web Visits / Month", options=std_categories, default="Low")
                web_purch_choice   = st.segmented_control("Web Purchases", options=std_categories, default="Low")
                cat_purch_choice   = st.segmented_control("Catalog Purchases", options=std_categories, default="Low")
            with col2:
                store_purch_choice = st.segmented_control("Store Purchases", options=std_categories, default="Medium")
                deal_purch_choice  = st.segmented_control("Deal Purchases", options=std_categories, default="Low")
            num_web_visits  = val_map["visits"].get(visit_choice, 3)
            num_web_purch   = val_map["web"].get(web_purch_choice, 4)
            num_cat_purch   = val_map["cat"].get(cat_purch_choice, 4)
            num_store_purch = val_map["store"].get(store_purch_choice, 7)
            num_deals_purch = val_map["deals"].get(deal_purch_choice, 2)
            st.header("Spending (Last 2 Years, $)", divider="gray")
            col1, col2 = st.columns(2)
            with col1:
                wines  = st.slider("Wines",  0, 1493, 174)
                meat   = st.slider("Meat",   0, 1000,  68)
                fruits = st.slider("Fruits", 0,  199,   8)
            with col2:
                fish   = st.slider("Fish",   0,  259,  12)
                sweets = st.slider("Sweets", 0,  262,   8)
                gold   = st.slider("Gold",   0,  321,  24)


        
    
    with left:
        with st.container(border=True):
            st.header("Recency & Past Campaigns", divider="gray")
            st.html("<hr style='margin: 2px 0px; border: none; border-top: 1px solid #31333F;'>")
            recency = st.slider("Days since last purchase", 0, 99, 49)
            col1, col2 = st.columns(2)
            with col1:
                accepted_cmp1 = int(st.toggle("Accepted Campaign 1 Offer"))
                accepted_cmp2 = int(st.toggle("Accepted Campaign 2 Offer"))
                accepted_cmp3 = int(st.toggle("Accepted Campaign 3 Offer"))
            with col2:
                accepted_cmp4 = int(st.toggle("Accepted Campaign 4 Offer"))
                accepted_cmp5 = int(st.toggle("Accepted Campaign 5 Offer"))
            
            entry = {
                # Demographics
                'Year_Birth': year_birth,
                'Income': income,
                'Education': education if education else "Graduation", # Fallback if None
                'Marital_Status': marital if marital else "Married",   # Fallback if None
                'Kidhome': kidhome,
                'Teenhome': teenhome,
                'Country': 'US', # HARDCODED DEFAULT: Required by your One-Hot Encoder
                
                # Spending
                'MntWines': wines,
                'MntMeatProducts': meat,
                'MntFruits': fruits,
                'MntFishProducts': fish,
                'MntSweetProducts': sweets,
                'MntGoldProds': gold,
                
                # Engagement (using mapped integers)
                'NumWebVisitsMonth': num_web_visits,
                'NumWebPurchases': num_web_purch,
                'NumCatalogPurchases': num_cat_purch,
                'NumStorePurchases': num_store_purch,
                'NumDealsPurchases': num_deals_purch,
                
                # Campaigns
                'Recency': recency,
                'AcceptedCmp1': accepted_cmp1,
                'AcceptedCmp2': accepted_cmp2,
                'AcceptedCmp3': accepted_cmp3,
                'AcceptedCmp4': accepted_cmp4,
                'AcceptedCmp5': accepted_cmp5
            }
            st.header("Response Probability", divider="gray")
            prob, impact_list = predicts_probs(
                entry, model, scaler, encoder, feature_cols, cap_bounds, artifacts
            )
            prob = int(prob * 100)
            # 1. Determine Status Color, Icon, and Text based on thresholds
            if prob < 33:
                status_icon = "✕"
                status_text = "Unlikely to respond"
                status_color = "#d85a30" 
            elif prob < 66:
                status_icon = "−"
                status_text = "Potential to respond"
                status_color = "#F5A623" 
            else:
                status_icon = "✓"
                status_text = "Likely to respond"
                status_color = "#00d26a" 

            # 2. Build the Plotly Gauge Chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob,
                number = {
                    'suffix': "%", 
                    'font': {'size': 48, 'color': '#1e9e76'} 
                },
                title = {
                    'text': "probability", 
                    'font': {'size': 14, 'color': '#888888'}
                },
                gauge = {
                    'axis': {'range': [0, 100], 'showticklabels': False, 'ticks': ''},
                    'bar': {'color': "#1e9e76", 'thickness': 0.4}, # The blue progress bar
                    'bgcolor': "#fff1d0", # The dark track behind the bar
                    'shape': "angular",
                }
            ))

            # 3. Clean up the layout to fit tightly in the Streamlit column
            fig.update_layout(
                margin=dict(l=10, r=10, t=20, b=0),
                height=200,
                paper_bgcolor="rgba(0,0,0,0)", # Transparent background
                font={'color': "white"}
            )

            # Render the chart
            st.plotly_chart(fig, width="stretch")
            st.markdown(f"""
                <div style="text-align: center; margin-top: -10px; margin-bottom: 16px;">
                    <span style="
                        font-size: 15px;
                        font-weight: 500;
                        color: {status_color};
                        background-color: {status_color}22;
                        padding: 6px 16px;
                        border-radius: 20px;
                        border: 1px solid {status_color}55;
                    ">
                        {status_icon} &nbsp; {status_text}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            st.space(size="small")
            
            
            
            
            # 1. Find the maximum absolute magnitude to scale the bars (0 to 100%)
            # Check if list is not empty to avoid division by zero errors
            if impact_list:
                max_mag = impact_list[0]["absolute_magnitude"] # Since it's sorted, the first is the biggest
            else:
                max_mag = 1 

            # 2. Build the HTML structure iteratively
            html_rows = ""
            
            # Loop through the top 6 most impactful features to keep the UI clean
            for item in impact_list[:6]:
                feat_name = item['feature']
                val = item['impact_value']
                mag = item['absolute_magnitude']
                
                # Calculate how wide the bar should be (capped at 100%)
                width_pct = min((mag / max_mag) * 100, 100)
                
                # Determine color and icon based on positive/negative impact
                if val >= 0:
                    color = "#00d26a" # Streamlit Green
                    icon = "+"
                else:
                    color = "#e24b4a" # Streamlit Red
                    icon = "−"
                    
                # Create the flex container for each row
                html_rows += f"""
                <div style="display: flex; align-items: center; margin-bottom: 12px; font-family: monospace;">
                    <div style="width: 20px; color: {color}; font-weight: bold; font-size: 16px;">{icon}</div>
                    <div style="width: 130px; color: #a0aab5; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{feat_name}</div>
                    <div style="flex-grow: 1; background-color: #888780; border-radius: 10px; height: 10px; margin-left: 10px;">
                        <div style="width: {width_pct}%; background-color: {color}; height: 100%; border-radius: 10px;"></div>
                    </div>
                </div>
                """

            # 3. Render the custom HTML
            st.markdown(html_rows, unsafe_allow_html=True)