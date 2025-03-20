import requests
import random
from flask import request, render_template, redirect, url_for, abort
from datamanager.sqlite_data_manager import SQLiteDataManager


db_file_name = 'data/moviebase.db'
data_manager = SQLiteDataManager(db_file_name)
app = data_manager.app


@app.route('/')
def home():
    """Returns a welcome message for the MovieWeb App."""
    movies = data_manager.get_user_movies(1) # Pick movies from "Admin"-User
    random_movies = random.sample(movies, min(len(movies), 3))

    for movie in random_movies:
        if movie.summary is None:
            movie.summary = "No summary available."

    return render_template('index.html', movies=random_movies)

@app.route('/users')
def list_users():
    """Fetches and returns a list of all users."""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)

@app.route('/users/<user_id>')
def list_user_movies(user_id):
    users = data_manager.get_all_users()
    user = next((user for user in users if user.id == int(user_id)), None)  # Get first match or None
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_movies.html', user=user, movies=movies) # {'movies': user_movies, 'username': user}

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    users = data_manager.get_all_users()

    if request.method == 'GET':
        return render_template('add_user.html', users=users)

    elif request.method == 'POST':
        name = request.form['name']
        pin = request.form['pin']
        email = request.form['email']

        if not name:
            return render_template('add_user.html', users=users)

        data_manager.add_user(name, pin, email)
        return redirect(url_for('list_users'))
        # return render_template('add_user.html', users=users)


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    movies = data_manager.get_user_movies(user_id)
    users = data_manager.get_all_users()
    user = next((user for user in users if int(user_id) == user.id), None)

    # Get message from URL parameters (if any)
    message = request.args.get('message')

    if request.method == 'GET':
        return render_template('add_movie.html', movies=movies, user_id=user_id, user=user, message=message)

    elif request.method == 'POST':
        title = request.form['title']

        # Fetch data from OMDb API
        try:
            title, rating, release_year, genre, summary, poster_image_url = data_manager.fetch_movie_data(title)
        except requests.exceptions.RequestException as e:
            abort(500, description=f"Failed to fetch data from OMDb API. Details: {e}")
        except KeyError:
            abort(404, description=f"No data found for '{title}' in OMDb.")
        except ValueError:
            return redirect(url_for('add_movie', user_id=user_id, message="Failed to find Movie in OMDB. Please Try again!"))
        # except Exception as e:
        #     abort(500, description=f"An unexpected error occurred: {e}")

        if not title:
            return f"Invalid movie data received for '{title}'. Please check the movie title."
        # Add to db
        data_manager.add_movie(title, rating, release_year, genre, summary, poster_image_url, user_id=user_id)
        return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<user_id>/update_movie/<movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movies = data_manager.get_user_movies(user_id)
    movie = next((movie for movie in movies if int(movie_id) == movie.id), None)
    users = data_manager.get_all_users()
    user = next((user for user in users if int(user_id) == user.id), None)

    if request.method == 'GET':
        return render_template('update_movie.html', user_id=user_id, user=user, movie=movie)

    elif request.method == 'POST':
        title = request.form['title']
        year = int(request.form['year'])
        rating = float(request.form['rating'])
        genre = request.form['genre']
        summary = request.form['summary']

        data_manager.update_movie(title, rating, year, genre, summary)

        return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['GET', 'POST'])
def delete_movie(user_id, movie_id):
    movies = data_manager.get_user_movies(user_id)
    movie = next((movie for movie in movies if movie.id == movie_id), None)
    users = data_manager.get_all_users()
    user = next((user for user in users if user.id == user_id), None)

    if request.method == 'POST':
        if movie:
            data_manager.delete_movie(movie_id)
        return redirect(url_for('list_user_movies', user_id=user_id))

    return render_template('delete_movie.html', movie=movie, user_id=user_id, user=user)

fi

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)