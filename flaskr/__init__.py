import sqlite3
from flask import Flask, g, request, jsonify, render_template
import os

# Path to this file's folder (flaskr)
BASE_DIR = os.path.dirname(__file__)

# Database file inside flaskr folder
DATABASE = os.path.join(BASE_DIR, 'notes.db')
SCHEMA = os.path.join(BASE_DIR, 'schema.sql')

def create_app():
    app = Flask(__name__)

    # --- Database helpers ---
    def get_db():
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE)
            db.row_factory = sqlite3.Row
        return db

    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    def init_db():
        """Initialize DB if it doesn't exist"""
        if not os.path.exists(DATABASE):
            with app.app_context():
                db = get_db()
                with open(SCHEMA, 'r') as f:
                    db.executescript(f.read())
                db.commit()
                print("Database initialized!")

    # --- Initialize DB on startup ---
    with app.app_context():
        init_db()

    # --- CRUD Routes ---

    # Create note
    @app.route('/notes', methods=['POST'])
    def create_note():
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            return jsonify({"error": "Title and content required"}), 400
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO notes (title, content) VALUES (?, ?)", (title, content)
        )
        db.commit()
        return jsonify({"id": cursor.lastrowid, "title": title, "content": content}), 201

    # Get all notes
    @app.route('/notes', methods=['GET'])
    def get_notes():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = [dict(row) for row in cursor.fetchall()]
        return jsonify(notes)

    # Get a single note
    @app.route('/notes/<int:note_id>', methods=['GET'])
    def get_note(note_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({"error": "Note not found"}), 404
        return jsonify(dict(row))

    # Update note
    @app.route('/notes/<int:note_id>', methods=['PUT'])
    def update_note(note_id):
        data = request.json
        title = data.get('title')
        content = data.get('content')
        if not title or not content:
            return jsonify({"error": "Title and content required"}), 400
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE notes SET title = ?, content = ? WHERE id = ?",
            (title, content, note_id)
        )
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Note not found"}), 404
        return jsonify({"id": note_id, "title": title, "content": content})

    # Delete note
    @app.route('/notes/<int:note_id>', methods=['DELETE'])
    def delete_note(note_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        db.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Note not found"}), 404
        return jsonify({"status": "deleted", "id": note_id})
    
    @app.route('/add_note', methods=['POST'])
    def add_note_form():
        title = request.form.get('title')
        content = request.form.get('content')
        if not title or not content:
            return "Title and content required", 400
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
        db.commit()
        return '', 302, {'Location': '/'}  # redirect back to home page

    @app.route('/')
    def home():
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        notes = [dict(row) for row in cursor.fetchall()]
        return render_template('index.html', notes=notes)

    return app