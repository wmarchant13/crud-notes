import sqlite3
import os
from flask import g, current_app

def get_db():
    """Get a SQLite connection. One per request stored in g."""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row  # rows behave like dicts
    return g.db

def close_db(e=None):
    """Close the database connection at the end of request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, mode='r') as f:
        db.executescript(f.read())
    db.commit()