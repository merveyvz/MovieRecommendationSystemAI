import streamlit as st


def render_movie_input():
    st.subheader("Enter Your Top 3 Favorite Movies")
    favorite_movies = []
    for i in range(3):
        movie = st.text_input(f"Favorite Movie {i + 1}")
        if movie:
            favorite_movies.append(movie)
    return favorite_movies
