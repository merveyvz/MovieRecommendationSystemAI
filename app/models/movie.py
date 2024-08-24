from sqlalchemy import Column, Integer, String, Float, Date

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String)
    release_date = Column(Date)
    rating = Column(Float)
    overview = Column(String)
    poster_path = Column(String)
