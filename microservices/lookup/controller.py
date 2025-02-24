import os
from dotenv import load_dotenv
import requests


class LookupController:
    def convert_fragment(self, files):
        load_dotenv()
        AUDD_KEY = os.getenv('AUDD_KEY')
                
        # Check request
        if not files: return {'error': 'Missing audio file'}, 400
        if len(files) > 1: return {'error': 'Multiple audio files detected'}, 400
        audio_fragment = files.get('file')
        if not audio_fragment.filename.endswith('.wav'): return {'error': 'Invalid audio file format, expected .wav'}, 400
                        
        response = requests.post(
            'https://api.audd.io/',
            data = {
                'api_token': AUDD_KEY,
                'return': 'timecode,apple_music,deezer,spotify',
            },
            files = {'file': audio_fragment}
        )
                
        if response.status_code != 200: return {'error': 'Failed to process audio fragment'}, 500
        response_json = response.json()
        if response_json['status'] == 'error': return {'error': 'Failed to process audio fragment'}, 500
        if response_json['status'] != 'success': return {'error': 'Failed to identify track'}, 500
                
        full_track = {
            'name': response_json['result']['title'],
            'artist': response_json['result']['artist'],
            'album': response_json['result']['album'],
            'genre': response_json['result']['genre'],
            'duration': response_json['result']['duration'],
        }
                
        response = requests.get(
            '127.0.0.1:5000/catalogue/tracks/list'
        )
        
        if response.status_code != 200: return {'error': 'Failed to retrieve track list'}, 500
        response_json = response.json()
        if 'error' in response_json: return {'error': 'Failed to retrieve track list'}, 500
        if 'tracks' not in response_json: return {'error': 'Failed to retrieve track list'}, 500
        
        tracks = response_json['tracks']
        
        print(tracks)       
        
        return {'full_track': full_track}, 200
