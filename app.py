from flask_sqlalchemy import SQLAlchemy
from datamanager.sqlite_data_manager import SQLiteDataManager

# Initialize SQLiteDataManager with the database file
db = SQLAlchemy()

db_file_name = 'data/moviebase.db'
data_manager = SQLiteDataManager(db_file_name)
app = data_manager.app


@app.route('/')
def home():
    """Returns a welcome message for the MovieWeb App."""
    return "Welcome to MovieWeb App!"

@app.route('/users')
def list_users():
    """Fetches and returns a list of all users."""
    users = data_manager.get_all_users()
    return str(users)  # Temporarily returning users as a string

if __name__ == '__main__':
    app.run(debug=True)