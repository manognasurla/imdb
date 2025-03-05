import streamlit as st
import pandas as pd
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load IMDb dataset
df = pd.read_csv("imdb_movies.csv")

# Preprocessing
scaler = StandardScaler()
numerical_features = ["budget_x", "revenue"]
df[numerical_features] = scaler.fit_transform(df[numerical_features])

df['score_category'] = pd.cut(df['score'], bins=[-float('inf'), 5, 7, float('inf')], labels=['low', 'medium', 'high'])

x = df[["budget_x", "revenue", 'names', 'date_x', 'country']]
y = df["score_category"]

# Encode categorical features
label_encoders = {}
for col in x.select_dtypes(include=['object']).columns:
    le = LabelEncoder()
    x[col] = le.fit_transform(x[col])
    label_encoders[col] = le

# Split data
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, random_state=42)

# Train LDA model
lda = LinearDiscriminantAnalysis()
lda.fit(x_train, y_train)
y_pred = lda.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)

# Streamlit UI
st.title("IMDb Movie Score Classification")
st.write("Classifying movies into score categories: Low, Medium, and High.")

st.write(f"Model Accuracy: {accuracy:.2f}")

# User Input for Prediction
st.subheader("Predict Movie Score Category")
budget = st.number_input("Enter Budget", min_value=0.0, step=100000.0)
revenue = st.number_input("Enter Revenue", min_value=0.0, step=100000.0)

if st.button("Predict"):
    user_data = np.array([[budget, revenue, 0, 0, 0]])  # Default encoded values for categorical fields
    user_data[:, :2] = scaler.transform(user_data[:, :2])  # Scale numerical values
    prediction = lda.predict(user_data)[0]
    st.write(f"Predicted Score Category: {prediction}")

