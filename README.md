# crud-notes

A simple CRUD web application built with Python using the Flask framework and SQLite. It allows notes to create, view, edit, and delete notes through a minimal web interface using HTML templates.

Here’s a simple step‑by‑step of how the app works:

create_app() builds the Flask app and wires everything together.

Database file: flaskr/notes.db; schema is in flaskr/schema.sql.

get_db(): on each request it opens (or returns) a sqlite3 connection stored on flask.g and sets row_factory so rows can be converted to dicts.

@app.teardown_appcontext: closes the DB connection after the request finishes.

init_db(): on startup (with app.app_context()) it creates the DB from schema.sql if notes.db doesn’t exist.

Routes (HTTP endpoints):

GET / -> home(): reads all notes, renders templates/index.html with notes (server-rendered HTML).

POST /add_note -> add_note_form(): handles an HTML form (request.form), inserts a note, then redirects back to /.

GET /notes -> get_notes(): returns all notes as JSON (useful for JS or API clients).

POST /notes -> create_note(): accepts JSON (request.json) to create a note, returns the new note and id.

GET /notes/<id> -> get_note(): returns one note as JSON or 404 if missing.

PUT /notes/<id> -> update_note(): accepts JSON to update title/content, checks rowcount to detect missing note.

DELETE /notes/<id> -> delete_note(): deletes note, checks rowcount and returns status or 404.

DB operations: use cursor.execute(...), db.commit(), cursor.lastrowid for new IDs, cursor.rowcount to see affected rows.

Typical web flow:

Browser requests / -> server queries DB and sends HTML with notes.

Submitting the HTML form POSTs to /add_note -> server inserts and redirects.

Frontend JS could call the /notes JSON endpoints to create/update/delete notes dynamically.

Initialization (no CLI)

- One-off script: run `python3 init_db.py` to create the database from `schema.sql`.
- Automatic on startup: the app will create the DB file if missing when run with `python3 app.py` or on first request.

CLI (optional): set `FLASK_APP=app` and use `flask init-db` to initialize via Flask CLI.
