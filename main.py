import streamlit as st
from app.views.genre_selection import render_genre_selection
from app.views.movie_input import render_movie_input
from app.views.movie_recommendations import render_popular_movies, render_recommended_movies
from app.services import get_movie_recommendations
from app.database import init_db


def load_css():
    with open("static/styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


@st.cache_resource
def initialize_database():
    init_db()


def main():
    st.set_page_config(page_title="Movie Recommendations By AI", layout="wide")

    load_css()
    initialize_database()

    # Center the title
    st.markdown("<h1 class='centered-title'>Movie Recommendations By AI</h1>", unsafe_allow_html=True)

    # Create three columns for the main layout
    left_col, center_col, right_col = st.columns([2, 5, 2])

    # Render popular movies in left and right columns
    render_popular_movies(left_col, right_col)

    with center_col:
        # Render genre selection
        selected_genres = render_genre_selection()

        # Render movie input
        favorite_movies = render_movie_input()

        if st.button("Get Recommendations"):
            if selected_genres and favorite_movies:
                with st.spinner("Fetching recommendations..."):
                    recommendations = get_movie_recommendations(selected_genres, favorite_movies)
                    render_recommended_movies(recommendations)
            else:
                st.warning("Please select at least one genre and enter your favorite movies.")


if __name__ == "__main__":
    main()
