"""
Top-level runner wrapper. Import the Flask `app` instance from the
`app` package and run it when executed directly. Keeping this small
avoids the `app` module/package name conflict.
"""
from app import app, ensure_db_exists

if __name__ == "__main__":
    ensure_db_exists()
    app.run(debug=True, port=8000)