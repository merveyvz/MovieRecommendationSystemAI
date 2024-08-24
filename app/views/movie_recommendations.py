import streamlit as st
from app.services import get_popular_movies, get_movie_details


def custom_card(title, year, rating, image_url):
    st.markdown(
        f"""
        <div style="
            background-image: url('{image_url}');
            background-size: cover;
            background-position: center;
            height: 300px;
            width: 100%;
            max-width: 200px;
            border-radius: 10px;
            position: relative;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            overflow: hidden;
        ">
            <div style="
                position: absolute;
                bottom: 0;
                left: 0;
                right: 0;
                height: 100%;
                background: linear-gradient(to top, rgba(0,0,0,0.9) 0%, rgba(0,0,0,0.7) 30%, rgba(0,0,0,0) 100%);
                padding: 10px;
                display: flex;
                flex-direction: column;
                justify-content: flex-end;
            ">
                <h4 style="margin: 0; color: white; font-size: 18px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">{title[:40] + ('...' if len(title) > 40 else '')}</h4>
                <p style="margin: 5px 0 0 0; color: #eee; font-size: 14px; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">{year}</p>
                <p style="margin: 0; color: #ffd700; font-size: 16px; font-weight: bold; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">{rating:.2f}/10</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def display_movie_cards(movies, column):
    for movie in movies:
        with column:
            custom_card(
                title=movie['title'],
                year=movie['release_date'][:4],
                rating=movie['rating'],
                image_url=movie['poster_path']
            )


def render_popular_movies(left_col, right_col):
    popular_movies = get_popular_movies()

    if popular_movies:
        with left_col:
            display_movie_cards(popular_movies[:7], left_col)
        with right_col:
            display_movie_cards(popular_movies[7:], right_col)
    else:
        st.info("Loading popular movies...")


def render_recommended_movies(recommendations):
    st.header("Recommended Movies")
    movie_details = []
    for movie in recommendations:
        details = get_movie_details(movie)
        if details:
            movie_details.append(details)

    if movie_details:
        for movie in movie_details:

            col1, col2 = st.columns([1, 2])

            with col1:
                custom_card(
                    title=movie['title'],
                    year=movie['release_date'][:4],
                    rating=movie['rating'],
                    image_url=movie['poster_path']
                )
            with col2:
                st.write(f"**Title:** {movie['title']}")
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"**Overview:** {movie['overview']}")
    else:
        st.warning("No movie details found for the recommendations.")