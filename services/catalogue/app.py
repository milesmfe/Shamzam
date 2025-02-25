from flask import Flask, Blueprint, request
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest
from services.catalogue.extensions import db
import os

from shared.utils import (
    format_response,
    generate_audio_hash,
    handle_errors,
    validate_file_upload
)

# Load environment variables
load_dotenv()

# Models
class Track(db.Model):
    """Database model for music tracks"""
    __tablename__ = 'tracks'
    
    id = db.Column(db.String(64), primary_key=True)  # SHA-256 hash
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    audio_file = db.Column(db.LargeBinary, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist
        }

# Routes
tracks_bp = Blueprint('tracks', __name__)

@tracks_bp.route('/', methods=['POST'])
@handle_errors
def add_track():
    """Handle file upload and track metadata"""
    # Validate file upload
    audio_file = validate_file_upload('audio_file')  # From shared/utils.py
    
    # Get form fields
    title = request.form.get('title')
    artist = request.form.get('artist')
    
    # Validate required fields
    if not title or not artist:
        raise BadRequest("Missing title or artist in form data")
    
    # Generate hash from audio bytes
    audio_bytes = audio_file.read()
    audio_hash = generate_audio_hash(audio_bytes)
    
    # Check for duplicates
    if Track.query.get(audio_hash):
        return format_response(
            status=409,
            message="Track already exists in catalogue"
        )
    
    # Create and save track
    new_track = Track(
        id=audio_hash,
        title=title,
        artist=artist,
        audio_file=audio_bytes
    )
    db.session.add(new_track)
    db.session.commit()
    
    return format_response(
        data=new_track.serialize(),
        status=201,
        message="Track added successfully"
    )

@tracks_bp.route('/<string:track_id>', methods=['DELETE'])
@handle_errors
def remove_track(track_id):
    """Endpoint for S2: Remove track from catalogue"""
    track = Track.query.get(track_id)
    
    if not track:
        return format_response(
            status=404,
            message="Track not found"
        )
    
    db.session.delete(track)
    db.session.commit()
    
    return format_response(
        status=204,
        message="Track deleted successfully"
    )

@tracks_bp.route('/', methods=['GET'])
@handle_errors
def list_tracks():
    """Endpoint for S3: List all tracks in catalogue"""
    tracks = Track.query.all()
    return format_response(
        data=[t.serialize() for t in tracks],
        message="Catalogue retrieved successfully"
    )

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    # Configure application
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(tracks_bp, url_prefix='/tracks')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

# Initialize app instance
app = create_app()

if __name__ == '__main__':
    app.run()