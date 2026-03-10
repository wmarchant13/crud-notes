# Imports
from flask import Flask
from app.database.database import close_db, init_db
from .routes.note_routes import bp as note_bp
import os

# Configure app and database
app = Flask(__name__)
app.config['DATABASE'] = 'database.db'

# Register teardown to close DB after request and register blueprint
app.teardown_appcontext(close_db)
app.register_blueprint(note_bp)


# Ensure DB exists: can be run automatically on startup or via the script
def ensure_db_exists():
    db_path = app.config.get('DATABASE', 'database.db')
    if not os.path.exists(db_path):
        # Ensure we run init_db() inside an application context so this
        # function can be called from the top-level runner (outside requests).
        with app.app_context():
            init_db()

# To ensure - initialize lazily on the first incoming request. Use a flag to run once.
_db_initialized = False

# Before request ensure it is initialized
@app.before_request
def ensure_db_before_request():
    global _db_initialized
    if not _db_initialized:
        ensure_db_exists()
        _db_initialized = True

