import base64
import os
from flask import Flask, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
from werkzeug.middleware.proxy_fix import ProxyFix

from services.catalogue.extensions import db
from services.catalogue.track import Track
from shared.utils import (
    format_response,
    generate_audio_hash,
    handle_errors,
    validate_audio_format,
    validate_file_upload
)

def create_app():
    """Application factory function"""
    app = Flask(__name__)
    
    CORS(app, resources={r"/tracks/*": {"origins": "*"}})
    
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1,
        x_proto=1,
        x_host=1,
    )
    
    # Configure application
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
    # Routes
    @app.route('/tracks/health')
    def health():
        return 'Catalogue operational', 200

    @app.route('/tracks/', methods=['POST'])
    @handle_errors
    def add_track():
        """Handle file upload and track metadata"""
        # Validate file upload
        audio_file = validate_file_upload('audio_file')  # From shared/utils.py
        
        validate_audio_format(audio_file.filename)
        
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

    @app.route('/tracks/<string:track_id>', methods=['DELETE'])
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

    @app.route('/tracks/', methods=['GET'])
    @handle_errors
    def list_tracks():
        """Endpoint for S3: List all tracks in catalogue"""
        tracks = Track.query.all()
        return format_response(
            data=[t.serialize() for t in tracks],
            message="Catalogue retrieved successfully"
        )
        
    @app.route('/tracks/<string:track_id>', methods=['GET'])
    @handle_errors
    def get_track(track_id):
        track = Track.query.get_or_404(track_id)
        
        # Encode audio bytes to proper base64
        audio_base64 = base64.b64encode(track.audio_file).decode('utf-8')
        
        return format_response(
            data={
                'id': track.id,
                'title': track.title,
                'artist': track.artist,
                'audio_file': audio_base64
            },
            message="Track details retrieved"
        )

    @app.route('/tracks/search', methods=['GET'])
    @handle_errors
    def search_tracks():
        """Search tracks by title and/or artist"""
        title = request.args.get('title')
        artist = request.args.get('artist')
        
        query = Track.query
        if title: query = query.filter(Track.title.ilike(f'%{title}%'))
        if artist: query = query.filter(Track.artist.ilike(f'%{artist}%'))
        
        tracks = query.all()
        return format_response(
            data=[t.serialize() for t in tracks],
            message="Search results"
        )
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='localhost',
        port=5000,
        threaded=True,
        debug=False
    )