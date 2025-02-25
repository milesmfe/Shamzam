# recognition_service/app.py
from flask import Flask, jsonify, request
from shared.utils import handle_errors, validate_file_upload
import requests
import os

app = Flask(__name__)
app.config['AUDD_API_KEY'] = os.getenv('AUDD_API_KEY')

@app.route('/recognize', methods=['POST'])
@handle_errors
def recognize():
    """Temporary implementation for S4 using AudD.io API"""
    audio_data = validate_file_upload()
    
    response = requests.post(
        "https://api.audd.io/recognize",
        files={'file': audio_data},
        data={'api_token': app.config['AUDD_API_KEY']}
    )
    response.raise_for_status()
    
    result = response.json().get('result')
    if not result:
        return jsonify({'error': 'No match found'}), 404
        
    return jsonify({
        'title': result.get('title'),
        'artist': result.get('artist'),
        'album': result.get('album', '')
    })

if __name__ == '__main__':
    app.run()
