import pandas as pd
import joblib

# Serialization Directory
FOLDER = 'Serialization'

def load_objects():
    model = joblib.load(f'{FOLDER}/model.pkl')
    scaler =  joblib.load(f'{FOLDER}/scaler.pkl')
    encoder = joblib.load(f'{FOLDER}/encoder.pkl')
    features = joblib.load(f'{FOLDER}/features.pkl')
    capped_bounds = joblib.load(f'{FOLDER}/cap_bounds.pkl')
    artifacts = joblib.load(f'{FOLDER}/artifacts.pkl')
    return model, scaler, encoder, features, capped_bounds, artifacts

def predicts_probs(entry, model, scaler, encoder, features, capped_bounds, artifacts):
    df = pd.DataFrame([entry])
    df.head()
    # Feature Engineering
    df['Age'] = 2014 - df['Year_Birth']
    df.drop(columns="Year_Birth")
    df['Total_Children'] = df['Kidhome'] + df['Teenhome']
    df['Total_Spent'] = (df['MntWines'] + df['MntFruits'] + df['MntMeatProducts'] +
                        df['MntFishProducts'] + df['MntSweetProducts'] + df['MntGoldProds'])
    df['Total_Accepted_Cmp'] = (df['AcceptedCmp1'] + df['AcceptedCmp2'] + df['AcceptedCmp3'] +
                                df['AcceptedCmp4'] + df['AcceptedCmp5'])
    df['Total_Accepted_Cmp'] = pd.to_numeric(df['Total_Accepted_Cmp'])

    # Encoding
    df['Education'] = df['Education'].map(artifacts['education_order'])
    ohe = pd.DataFrame(
        encoder.transform(df[['Marital_Status', 'Country']]),
        columns=encoder.get_feature_names_out(['Marital_Status', 'Country'])
    )
    df = df.drop(columns=['Marital_Status', 'Country']).join(ohe)
    expected_features = scaler.feature_names_in_
    
    # Column Alignment
    df = df.reindex(columns=expected_features, fill_value=0)
    
    # Scale & Predict
    scaled = scaler.transform(df)
    prob = model.predict_proba(scaled)[:, 1][0]
    
    # Feature Importance
    coefs = model.coef_[0]
    scaled_inputs = scaled[0] 
    impacts = coefs * scaled_inputs
    
    # Build the list of dictionaries
    impact_list = []
    for name, impact in zip(expected_features, impacts):
        impact_list.append({
            "feature": name,
            "impact_value": float(impact), 
            "absolute_magnitude": abs(float(impact))
        })
    impact_list.sort(key=lambda x: x["absolute_magnitude"], reverse=True)
    
    return round(prob, 4), impact_list

    
