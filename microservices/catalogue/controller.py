import datetime
import os
import sqlite3

from dotenv import load_dotenv


class CatalogueController:
    def add_track(self, request):
        required_fields = {'name', 'artist', 'album', 'genre', 'duration'}
        
        # Check request
        if not request: return {'error': 'Missing required fields'}, 400
        if not all(field in request for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        load_dotenv()
        DATABASE_PATH = os.getenv('DATABASE_PATH')
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tracks (name, artist, album, genre, duration, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (request['name'], request['artist'], request['album'], request['genre'], request['duration'], datetime.datetime.now()))
        
        track_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {'message': 'Track added successfully', 'track_id': track_id}, 201
    
    def get_track(self, id):
        
        # Check id
        if not id: return {'error': 'Track not specified'}, 400
        if not id.isdigit(): return {'error': 'Invalid track id'}, 400
        
        load_dotenv()
        DATABASE_PATH = os.getenv('DATABASE_PATH')
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tracks WHERE id = ?', (id,))
        track = cursor.fetchone()
        conn.close()
        
        if not track:
            return {'error': 'Track not found'}, 404
        
        track_data = {
            'id': track[0],
            'name': track[1],
            'artist': track[2],
            'album': track[3],
            'genre': track[4],
            'duration': track[5],
            'created_at': track[6]
        }
        
        return {'track': track_data}, 200
        
    def remove_track(self, id):
        
        # Check id
        if not id: return {'error': 'Track not specified'}, 400
        if not id.isdigit(): return {'error': 'Invalid track id'}, 400
        
        # TODO: Check if track exists in database
        
        # TODO: Database connection: Remove track from database
        return {'message': 'Track removed successfully'}, 200
    
    def list_tracks(self):
        # TODO: Database connection: Get all tracks from database
        tracks = [{'id': i, 'name': f'Track {i}', 'artist': f'Artist {i}', 'album': f'Album {i}', f'genre': f'Genre {i}', 'duration': i*100} for i in range(5)]
        
        return {'tracks': tracks}, 200