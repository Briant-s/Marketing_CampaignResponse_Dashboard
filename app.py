import streamlit as st
from pipeline import load_objects, predicts_probs

st.set_page_config(page_title='Campaign Response Predictor', layout='wide')

@st.cache_resource
def load():
    return load_objects()

model, scaler, encoder, cap_bounds, feature_cols, artifacts = load()

st.title('Campaign Response Predictor')

col1, col2 = st.columns(2)

with col1:
    year_birth  = st.slider('Birth Year', 1940, 1999, 1975)
    income      = st.number_input('Annual Income ($)', 0, 200000, 52000)
    recency     = st.slider('Days Since Last Purchase', 0, 99, 49)
    marital     = st.selectbox('Marital Status', ['Single', 'Married', 'Divorced', 'Together', 'Widow'])
    education   = st.selectbox('Education', ['Basic', 'Bachelor', 'Master', 'PhD'])
    country     = st.selectbox('Country', ['Spain', 'Canada', 'USA', 'Australia', 'Germany', 'India', 'Saudi Arabia', 'Mexico'])
    kidhome     = st.number_input('Kids at Home', 0, 3, 0)
    teenhome    = st.number_input('Teens at Home', 0, 3, 0)

with col2:
    wines       = st.slider('Wines Spend ($)', 0, 1500, 174)
    meat        = st.slider('Meat Spend ($)', 0, 1000, 68)
    fruits      = st.slider('Fruits Spend ($)', 0, 200, 8)
    fish        = st.slider('Fish Spend ($)', 0, 260, 12)
    sweets      = st.slider('Sweets Spend ($)', 0, 263, 8)
    gold        = st.slider('Gold Spend ($)', 0, 322, 24)
    cmp1        = st.checkbox('Accepted Campaign 1')
    cmp2        = st.checkbox('Accepted Campaign 2')
    cmp3        = st.checkbox('Accepted Campaign 3')
    cmp4        = st.checkbox('Accepted Campaign 4')
    cmp5        = st.checkbox('Accepted Campaign 5')

customer = {
    'Year_Birth': year_birth, 'Income': income, 'Recency': recency,
    'Marital_Status': marital, 'Education': education, 'Country': country,
    'Kidhome': kidhome, 'Teenhome': teenhome,
    'MntWines': wines, 'MntMeatProducts': meat, 'MntFruits': fruits,
    'MntFishProducts': fish, 'MntSweetProducts': sweets, 'MntGoldProds': gold,
    'AcceptedCmp1': int(cmp1), 'AcceptedCmp2': int(cmp2), 'AcceptedCmp3': int(cmp3),
    'AcceptedCmp4': int(cmp4), 'AcceptedCmp5': int(cmp5),
    'NumWebPurchases': 0, 'NumCatalogPurchases': 0,
    'NumStorePurchases': 0, 'NumDealsPurchases': 0, 'NumWebVisitsMonth': 0
}

prob = predicts_probs(customer, model, scaler, encoder, cap_bounds, feature_cols, artifacts)
threshold = 0.15

st.divider()
col3, col4 = st.columns(2)
with col3:
    st.metric('Response Probability', f'{prob:.1%}')
with col4:
    if prob >= threshold:
        st.success('✅ Likely to respond — include in campaign')
    else:
        st.warning('⚠️ Unlikely to respond — consider excluding')