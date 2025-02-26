from flask import Flask, jsonify
import requests
import os
from shared.utils import handle_errors, validate_file_upload

def create_app():
    app = Flask(__name__)
    app.config['AUDD_API_KEY'] = os.getenv('AUDD_API_KEY')
    catalogue_host = os.getenv('CATALOGUE_INTERNAL_HOST')
    catalogue_port = os.getenv('CATALOGUE_INTERNAL_PORT')
    app.config['CATALOGUE_INTERNAL_URL'] = f"http://{catalogue_host}:{catalogue_port}/tracks"

    @app.route('/health')
    def health():
        return 'Recognition operational', 200

    @app.route('/recognize', methods=['POST'])
    @handle_errors
    def recognize():
        """Audio recognition and catalogue matching endpoint"""
        # 1. Validate audio file upload
        audio_file = validate_file_upload('audio_file')
        audio_bytes = audio_file.read()

        try:
            # 2. Recognize with AudD.io
            audd_response = requests.post(
                "https://api.audd.io/recognize",
                files={'file': (audio_file.filename, audio_bytes)},
                data={'api_token': app.config['AUDD_API_KEY']},
                timeout=10
            )
            audd_response.raise_for_status()
            
            audd_result = audd_response.json().get('result')
            if not audd_result:
                return jsonify({
                    "error": "No matching track found in recognition service",
                    "code": "NO_RECOGNITION_MATCH"
                }), 404

            # 3. Search catalogue for matches
            search_params = {
                'title': audd_result['title'],
                'artist': audd_result['artist']
            }
            catalogue_response = requests.get(
                f"{app.config['CATALOGUE_INTERNAL_URL']}/tracks/search",
                params=search_params,
                timeout=10 
            )
            
            if catalogue_response.status_code != 200:
                return jsonify({
                    "error": "Catalogue service unavailable",
                    "code": "CATALOGUE_ERROR"
                }), 502

            matches = catalogue_response.json().get('data', [])
            if not matches:
                return jsonify({
                    "error": "Recognized track not in catalogue",
                    "code": "CATALOGUE_MISSING",
                    "recognized_title": audd_result['title'],
                    "recognized_artist": audd_result['artist']
                }), 404

            # 4. Get full track details from catalogue
            track_id = matches[0]['id']
            track_response = requests.get(
                f"{app.config['CATALOGUE_INTERNAL_URL']}/tracks/{track_id}",
                timeout=10 
            )
            
            if track_response.status_code != 200:
                return jsonify({
                    "error": "Failed to retrieve track details",
                    "code": "TRACK_FETCH_ERROR"
                }), 502

            return jsonify(track_response.json()['data'])

        except requests.exceptions.Timeout:
            return jsonify({
                "error": "Request to external service timed out",
                "code": "TIMEOUT_ERROR"
            }), 504

    return app

app = create_app()

if __name__ == '__main__':
    app.run(
        host='recognition',
        port=5002,
        threaded=True,
        debug=False    
    )
