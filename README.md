# 🎬 Movie Recommendation System

## 📝 Overview

This Movie Recommendation System is a web application built with Python and Streamlit that provides personalized movie recommendations based on user preferences. It utilizes the OpenAI API for generating recommendations and the TMDb API for fetching movie details.

## ✨ Features

- User-friendly interface for selecting favorite movie genres and inputting favorite movies
- Display of popular movies updated daily
- Personalized movie recommendations based on user input
- Detailed movie information including title, year, rating, genre, and overview
- Movie cards featuring poster images and gradient overlays

## 🛠️ Technologies Used

- Python 3.8+
- Streamlit
- SQLAlchemy
- OpenAI API
- TMDB API
- aiohttp for asynchronous API requests

## 🚀 Installation

1. Clone the repository:
   ``` bash
   git clone https://github.com/merveyvz/MovieRecommendationSystem.git

   ```
2. Install the required packages:
   ``` bash
   pip install -r requirements.txt
   ```

3. Add your API keys to `.env` file:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   TMDB_API_KEY=your_tmdb_api_key_here
   DATABASE_URL=sqlite:///./movies.db
   ```

## 📖 Usage

1. Run the Streamlit app:
   ``` bash
   streamlit run main.py
   ```

2. Open your web browser and go to `http://localhost:8501`

3. Select your favorite movie genres and enter your top 3 favorite movies

4. Click "Get Recommendations" to receive personalized movie suggestions

## 📁 Project Structure

- `app/`: Main application package
  - `models/`: Database models (SQLAlchemy ORM classes)
  - `services/`: Business logic, API interactions (OpenAI, TMDb)
  - `views/`: Streamlit UI components and layouts
  - `config.py`: Configuration settings (API keys, database URL)
  - `database.py`: Database connection and session management

- `static/`: Static files
  - `styles.css`: Custom CSS for styling the Streamlit app

- `.env`: Environment variables (API keys, database URL)

- `requirements.txt`: List of Python package dependencies


## 🙏 Acknowledgements

- [OpenAI](https://platform.openai.com/docs/overview) for providing the GPT model used in generating recommendations
- [TMDB](https://developer.themoviedb.org/reference/intro/getting-started) for their comprehensive movie database and API
- Streamlit for the excellent web app framework