# crud-notes

A simple CRUD web application using Flask + SQLite. The repo contains the app, templates, and a SQL schema — the database file itself is intentionally not tracked.

Quick start (local development)

1. Create and activate a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Initialize the database (required on a fresh clone)

```bash
python3 init_db.py
```

This creates the SQLite database file configured in `app.config['DATABASE']` (default: `database.db`). The SQL schema lives in `schema.sql`.

4. Run the app:

```bash
python3 app.py
# then open http://127.0.0.1:8000/
```

Notes about repository history

- The local SQLite DB file is not tracked (see `.gitignore`). If you previously committed a DB file, it has been removed from the repository and purged from history;

App structure (short)

- `app/` — application package: routes, DB helpers, templates
- `app/templates/index.html` — main board UI
- `schema.sql` — SQL schema used by `init_db.py`
- `init_db.py` — one-off script that initializes the DB inside the application context

API & pages

- `GET /` — home page (server-rendered board UI)
- `POST /add_note` — form handler (HTML form -> redirect)
- `GET /notes` — list notes as JSON
- `POST /notes` — create note (JSON API)
- `PUT /notes/<id>` — update note (JSON)
- `DELETE /notes/<id>` — delete note (JSON)

Troubleshooting

- If the app raises "Working outside of application context" when running scripts, make sure DB initialization is executed inside the app context — `init_db.py` already does this.

Contributing

- Create feature branches, run tests/manual smoke tests, and open a PR.

License / notes

- Small demo app intended for learning; modify as you wish.
