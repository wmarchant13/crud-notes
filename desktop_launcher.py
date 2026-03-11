import webview
from threading import Thread
from app import app  # Import your Flask app object from app.py

# Function to start Flask server
def start_flask():
    # Make sure the port matches what your app normally uses
    app.run(port=8000, debug=False)

if __name__ == "__main__":
    # Start Flask in a separate thread
    flask_thread = Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # Open desktop window showing your Flask app
    webview.create_window("My Flask App", "http://127.0.0.1:8000")
    webview.start()

