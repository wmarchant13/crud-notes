from flask import request, jsonify, render_template, redirect, Blueprint
from app.service.note_service import NoteService, ServiceError

# Create a blueprint (no prefix so routes are mounted at root)
bp = Blueprint("notes", __name__, url_prefix="")

Note_service = NoteService()

# Create Note 
@bp.route('/notes', methods=['POST'])
def create_note():
    # JSON API endpoint: require application/json
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415
    data = request.get_json()
    try:
        note = Note_service.create_note(data['title'], data["content"])
        return jsonify({"id": note.id, "title": note.title, "content": note.content}), 201
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400


# Get all notes
@bp.route('/notes', methods=['GET'])
def get_notes():
    try:
        notes = Note_service.get_notes()
        return jsonify(notes)
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400

# Update note
@bp.route('/notes/<int:note_id>', methods=['PUT'])
def update_note(note_id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form
    try:
        note = Note_service.update_note(note_id, data['title'], data['content'])
        return jsonify({"id": note_id, "title": note.title, "content": note.content})
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400


# Delete note
@bp.route('/notes/<int:note_id>', methods=['DELETE'])
def delete_note(note_id):
    try:
        Note_service.delete_note(note_id)
        return jsonify({"status": "deleted", "id": note_id})
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400

# Handle Add Note Form
@bp.route('/add_note', methods=['POST'])
def add_note_form():
    # Browser form handler: prefer form fields, fallback to JSON
    title = request.form.get('title')
    content = request.form.get('content')
    if (not title or not content) and request.is_json:
        data = request.get_json()
        title = title or data.get('title')
        content = content or data.get('content')
    try:
        Note_service.create_note(title, content)
        return redirect('/')
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400


# Home page
@bp.route('/')
def home():
    try:
        notes = Note_service.home()
        return render_template('index.html', notes=notes)
    except ServiceError as e:
        return jsonify({"error": str(e)}), 400