import requests
import pandas as pd
import streamlit as st

# IMDb API details
IMDB_HOST = "imdb-com.p.rapidapi.com"
IMDB_API_KEY = "adbee7169amshb7f94a54c3f881bp1ea346jsn4753ffc1e693"
IMDB_URL = f"https://{IMDB_HOST}/title/get-overview"

# Function to fetch movie data
def get_movie_data(movie_id):
    headers = {
        "X-RapidAPI-Host": IMDB_HOST,
        "X-RapidAPI-Key": IMDB_API_KEY
    }
    params = {"tconst": movie_id}  # IMDb ID of the movie
    response = requests.get(IMDB_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to clean and format data
def clean_movie_data(data):
    if not data:
        return None
    
    cleaned_data = {}
    fields = ["title", "year", "ratings", "plotSummary", "genres", "directors", "actors"]
    
    for field in fields:
        if field in data:
            cleaned_data[field] = data[field]
    
    # Convert ratings to a structured format
    if "ratings" in cleaned_data:
        cleaned_data["ratingValue"] = cleaned_data["ratings"].get("ratingValue", "N/A")
        cleaned_data["ratingCount"] = cleaned_data["ratings"].get("ratingCount", "N/A")
        del cleaned_data["ratings"]
    
    return cleaned_data

# Streamlit UI
st.title("IMDb Movie Data Fetcher")
st.write("Enter the IMDb Movie ID to get its details.")

movie_id = st.text_input("Enter IMDb ID (e.g., tt0111161 for The Shawshank Redemption):")

if st.button("Fetch Movie Data"):
    raw_data = get_movie_data(movie_id)
    cleaned_data = clean_movie_data(raw_data)
    
    if cleaned_data:
        st.json(cleaned_data)  # Display cleaned JSON data in Streamlit
    else:
        st.error("Movie not found or error fetching data.")
