import pandas as pd
import numpy as np
import streamlit as st
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split

# Load IMDb dataset
df = pd.read_csv("imdb_movies.csv")

# Preprocess data
scaler = StandardScaler()
numerical_features = ["budget_x", "revenue"]
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# Categorize 'score' into 'low', 'medium', 'high'
df['score_category'] = pd.cut(df['score'], bins=[-float('inf'), 5, 7, float('inf')], labels=['low', 'medium', 'high'])

# Select features and target
x = df[["budget_x", "revenue", 'names', 'date_x', 'country']]
y = df["score_category"]

# Encode categorical variables
label_encoders = {}
for col in x.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    x[col] = le.fit_transform(x[col])
    label_encoders[col] = le

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

# Train LDA model
lda = LinearDiscriminantAnalysis()
lda.fit(x_train, y_train)

# Streamlit UI
st.title("IMDb Movie Score Prediction")
st.write("Enter movie details to predict its IMDb score category (Low, Medium, High).")

# User input fields
budget = st.number_input("Budget", min_value=0.0)
revenue = st.number_input("Revenue", min_value=0.0)
name = st.text_input("Movie Name")
date = st.text_input("Release Date")
country = st.text_input("Country")

# Convert inputs using label encoders if necessary
if name and date and country:
    if name in label_encoders['names'].classes_:
        name_encoded = label_encoders['names'].transform([name])[0]
    else:
        name_encoded = 0  # Default for unknown values
    
    if date in label_encoders['date_x'].classes_:
        date_encoded = label_encoders['date_x'].transform([date])[0]
    else:
        date_encoded = 0
    
    if country in label_encoders['country'].classes_:
        country_encoded = label_encoders['country'].transform([country])[0]
    else:
        country_encoded = 0

    # Prepare input data for prediction
    user_input = np.array([[budget, revenue, name_encoded, date_encoded, country_encoded]])
    user_input[:, :2] = scaler.transform(user_input[:, :2])  # Scale numerical features
    
    # Make prediction
    prediction = lda.predict(user_input)[0]
    st.write(f"Predicted IMDb Score Category: {prediction}")

