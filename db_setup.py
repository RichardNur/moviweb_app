from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# Create a database connection
engine = create_engine('sqlite:///data/moviebase.db')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

# Define the data table class's parent class
Base = declarative_base()

class User(Base):
    """User model representing users of the system."""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    movies = relationship('Movie', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


class Movie(Base):
    """Movie model representing movies associated with users."""
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    poster = Column(String(255), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f'<Movie {self.title}>'

# Create tables in DB:
Base.metadata.create_all(engine)

# Create an instance of the Restaurant table class

user1 = User(name="John Doe", email="johndoe@example.com")
movie1 = Movie(title="Inception", year=2010, rating=8.8, poster="https://example.com/inception.jpg",
               user_id=1)

# Since the session is already open, add the new restaurant record
session.add(user1)
session.add(movie1)
session.commit()