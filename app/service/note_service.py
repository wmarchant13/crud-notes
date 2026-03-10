from app.repository.note_repository import NoteRepository

class ServiceError(Exception):
    pass

class NoteService:

    # Inititialize self
    def __init__(self):
        self.note_repository = NoteRepository()

    # Create Note
    def create_note(self, title, content):
        if not title or not content:
            return ServiceError('No Title or Content')
        try:
            note = self.note_repository.create_note(title, content)
            return note
        except ServiceError as e:
            raise ServiceError("Failed to create note") from e
    
    # Get All Notes
    def get_notes(self):
        return self.note_repository.get_notes()
    
    # Update Note
    def update_note(self, note_id, title, content):
        if not title or not content:
            return ServiceError('No Title or Content')
        try:
            note = self.note_repository.update_note(note_id, title, content)
            return note
        except ServiceError as e:
            raise ServiceError("Failed to update note") from e
    
   # Delete Note
    def delete_note(self, note_id):
        try:
            note = self.note_repository.delete_note(note_id)
            return note
        except ServiceError as e:
            raise ServiceError("Failed to delet note") from e
    
    # Handle Add Note Form
    def add_note_form(self, title, content):
        if not title or not content:
            return ServiceError('No Title or Content')
        try:
            note = self.note_repository.create_note(title, content)
            return note
        except ServiceError as e:
            raise ServiceError("Failed to create note from form") from e

   # Home page
    def home(self):
        try:
            note = self.note_repository.get_notes()
            return note
        except ServiceError as e:
            raise ServiceError("Failed to get notes") from e