from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """User model representing users of the system."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    movies = relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'


class Movie(db.Model):
    """Movie model representing movies associated with users."""
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    title = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    poster = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'