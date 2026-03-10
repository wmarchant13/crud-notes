# Imports
from app.models.note import Note
from app.database.database import get_db

class RepositoryError(Exception):
    pass

class NoteRepository:

    # Create Note 
    def create_note(self, title, content):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            db.commit()
            note = Note(id=cursor.lastrowid, title=title, content=content)
            return note
        except Exception as e:
            raise RepositoryError("DB query failed") from e

    # Get All Notes
    def get_notes(self):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            notes = [dict(row) for row in cursor.fetchall()]
            return notes
        except Exception as e:
            raise RepositoryError("DB query failed") from e

    # Update Note 
    def update_note(self, note_id, title, content):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                "UPDATE notes SET title = ?, content = ? WHERE id = ?",
                (title, content, note_id)
            )
            db.commit()
            if cursor.rowcount == 0:
                raise RepositoryError("Note not found")
            note = Note(id=note_id, title=title, content=content)
            return note
        except Exception as e:
            raise RepositoryError("DB query failed") from e
    
    # Delete Note 
    def delete_note(self, note_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
            db.commit()
            if cursor.rowcount == 0:
                raise RepositoryError("Note not found")
            return note_id
        except Exception as e:
            raise RepositoryError("DB query failed") from e
    
    # Home page display 
    def home(self):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            notes = [dict(row) for row in cursor.fetchall()]
            return notes
        except Exception as e:
            raise RepositoryError("DB query failed") from e