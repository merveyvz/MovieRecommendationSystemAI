import streamlit as st


def render_genre_selection():
    st.subheader("Select Your Favorite Genres")
    genres = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama",
        "Family", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance",
        "Science Fiction", "TV Movie", "Thriller", "War", "Western"
    ]
    selected_genres = st.multiselect("Choose one or more genres:", genres)
    return selected_genres
