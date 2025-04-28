# MovieWeb App

#### https://shaire.pythonanywhere.com/ - Visit us & share your favorite Movies with the community

This MovieWeb App is a web application that allows users to manage their movie lists, add and update movie details, and explore movie information fetched from the OMDb API. The application supports basic user management and interacts with an SQLite database to store movie data.

## Features

- **User Management**: Add and view users.
- **Movie List**: Each user has a personalized movie list.
- **Add/Update Movies**: Users can add and update movies with details like title, year, rating, genre, and summary.
- **OMDb Integration**: Fetch movie details such as rating, release year, genre, and summary from the OMDb API.

## Tech Stack

- **Backend**: Python (Flask)
- **Database**: SQLite
- **Frontend**: HTML, CSS (static styling)
- **API Integration**: OMDb API

## Installation

### Prerequisites

- Python 3.x
- Virtual environment (recommended)

### Steps

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/moviweb_app.git
    cd moviweb_app
    ```

2. Set up a virtual environment:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Set up the database:

    ```bash
    python db_setup.py
    ```

5. Run the application:

    ```bash
    flask run
    ```

6. Access the application by navigating to `http://127.0.0.1:5000` in your browser.

## Folder Structure
- **LICENSE**
- **__init__.py**
- **__pycache__/**
- **app.py**
- **data/**
  - `moviebase.db`
- **datamanager/**
  - `__init__.py`
  - `__pycache__/`
  - `data_manager_interface.py`
  - `models.py`
  - `sqlite_data_manager.py`
- **db_setup.py**
- **instance/**
- **requirements.txt**
- **static/**
  - `styles.css`
- **templates/**
  - `404.html`
  - `500.html`
  - `add_movie.html`
  - `add_user.html`
  - `database_error.html`
  - `delete_movie.html`
  - `index.html`
  - `update_movie.html`
  - `user_movies.html`
  - `users.html`

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a new pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OMDb API for movie data.
- Flask for the backend framework.
- SQLite for the database.
