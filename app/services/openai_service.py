import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY


def get_movie_recommendations(genres, favorite_movies):
    prompt = f"Recommend 5 movies based on these genres: {', '.join(genres)} and these favorite movies: {', '.join(favorite_movies)}. Only provide the movie titles, separated by commas."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a movie recommendation expert."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )

    recommendations = response.choices[0].message['content'].strip().split(", ")
    return recommendations[:5]  # Ensure we only return 5 recommendations