import pandas as pd
import streamlit as st
import joblib

FOLDER = "Serialization"


@st.cache_resource 
def load_objects():
    model        = joblib.load(f'{FOLDER}/model.pkl')
    scaler       = joblib.load(f'{FOLDER}/scaler.pkl')
    encoder      = joblib.load(f'{FOLDER}/encoder.pkl')
    features     = joblib.load(f'{FOLDER}/features.pkl')
    capped_bounds = joblib.load(f'{FOLDER}/cap_bounds.pkl')
    artifacts    = joblib.load(f'{FOLDER}/artifacts.pkl')
    return model, scaler, encoder, features, capped_bounds, artifacts

@st.cache_data
def load_data():
    df = pd.read_csv("Dataset/marketing_data.csv")
    df.columns = df.columns.str.strip()
    df["Age"] = 2024 - df["Year_Birth"]
    df["TotalSpend"] = (df["MntWines"] + df["MntFruits"] + df["MntMeatProducts"]
                        + df["MntFishProducts"] + df["MntSweetProducts"] + df["MntGoldProds"])
    df["TotalPurchases"] = (df["NumDealsPurchases"] + df["NumWebPurchases"]
                            + df["NumCatalogPurchases"] + df["NumStorePurchases"])
    df["AnyAccepted"] = (df[["AcceptedCmp1","AcceptedCmp2","AcceptedCmp3",
                               "AcceptedCmp4","AcceptedCmp5","Response"]].sum(axis=1) > 0).astype(int)
    df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"])
    df["Income"] = df["Income"].fillna(df["Income"].median())
    df["AgeGroup"] = pd.cut(df["Age"], bins=[17,30,40,50,60,100],
                             labels=["18–30","31–40","41–50","51–60","60+"])
    _, _, _, _, capped_bounds, _ = load_objects()
    for col, bounds in capped_bounds.items():
        if col in df.columns:
            lower, upper = bounds
            df[col] = df[col].clip(lower=lower, upper=upper)
    df["Marital_Status"] = df["Marital_Status"].replace(
        {'YOLO': 'Single', 'Alone': 'Single', 'Absurd': 'Single'}
    )
    df["Education"] = df["Education"].replace(
        {'2n Cycle': 'Master', 'Graduation': 'Bachelor'}
    )
    return df   



