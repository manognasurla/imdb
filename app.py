import requests
import pandas as pd
import streamlit as st

# IMDb API details
IMDB_HOST = "imdb-com.p.rapidapi.com"
IMDB_API_KEY = "adbee7169amshb7f94a54c3f881bp1ea346jsn4753ffc1e693"
SEARCH_URL = f"https://{IMDB_HOST}/title/v2/find"
MOVIE_URL = f"https://{IMDB_HOST}/title/get-overview"

# Function to get IMDb ID from movie name
def get_imdb_id(movie_name):
    headers = {
        "X-RapidAPI-Host": IMDB_HOST,
        "X-RapidAPI-Key": IMDB_API_KEY
    }
    params = {"q": movie_name, "limit": 5}  # Changed to 'q' parameter for better search
    response = requests.get(SEARCH_URL, headers=headers, params=params)
    
    st.write("Debug: Raw Search API Response", response.text)  # Log raw API response
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data and len(data["results"]) > 0:
            for result in data["results"]:
                if "id" in result and "/title/" in result["id"]:
                    imdb_id = result["id"].replace("/title/", "").replace("/", "")
                    st.write("Debug: Extracted IMDb ID", imdb_id)  # Debugging output
                    return imdb_id
    return None

# Function to fetch movie details
def get_movie_data(movie_id):
    headers = {
        "X-RapidAPI-Host": IMDB_HOST,
        "X-RapidAPI-Key": IMDB_API_KEY
    }
    params = {"tconst": movie_id}
    response = requests.get(MOVIE_URL, headers=headers, params=params)
    
    st.write("Debug: Raw Movie Data API Response", response.text)  # Log raw API response
    
    if response.status_code == 200:
        return response.json()
    return None

# Function to clean movie data
def clean_movie_data(data):
    if not data:
        return None
    
    cleaned_data = {}
    fields = ["title", "year", "ratings", "plotSummary", "genres", "directors", "actors"]
    
    for field in fields:
        if field in data:
            cleaned_data[field] = data[field]
    
    if "ratings" in cleaned_data:
        cleaned_data["ratingValue"] = cleaned_data["ratings"].get("ratingValue", "N/A")
        cleaned_data["ratingCount"] = cleaned_data["ratings"].get("ratingCount", "N/A")
        del cleaned_data["ratings"]
    
    return cleaned_data

# Streamlit UI
st.title("IMDb Movie Search")
st.write("Enter a movie name to fetch IMDb details.")

movie_name = st.text_input("Enter Movie Name:")

if st.button("Fetch Movie Data"):
    movie_id = get_imdb_id(movie_name)
    if movie_id:
        raw_data = get_movie_data(movie_id)
        cleaned_data = clean_movie_data(raw_data)
        
        if cleaned_data:
            st.json(cleaned_data)
        else:
            st.error("Movie details not found.")
    else:
        st.error("Movie not found. Please check the name.")
