import pytest
import base64
from catalogue.app import create_app, Track
from catalogue.extensions import db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
        with app.app_context():
            db.drop_all()

def test_add_track(test_client):
    """Test S1 with file upload"""
    with open('test_audio.wav', 'rb') as f:
        response = test_client.post('/tracks/', data={
            'title': 'Test Song',
            'artist': 'Test Artist',
            'audio_file': f
        }, content_type='multipart/form-data')
    
    assert response.status_code == 201
    assert 'Test Song' in response.json['data']['title']
    assert Track.query.count() == 1

def test_duplicate_track(test_client):
    """Test S1 unhappy path: Duplicate track"""
    audio_data = base64.b64encode(b"test_audio.wav").decode()
    
    # First submission
    test_client.post('/tracks/', json={
        'title': 'First',
        'artist': 'Artist',
        'audio_data': audio_data
    })
    
    # Duplicate submission
    response = test_client.post('/tracks/', json={
        'title': 'Duplicate',
        'artist': 'Artist',
        'audio_data': audio_data
    })
    
    assert response.status_code == 409
    assert 'already exists' in response.json['message']

def test_remove_track(test_client):
    """Test S2: Remove track"""
    audio_data = base64.b64encode(b"audio_to_delete").decode()
    
    # Add track
    add_res = test_client.post('/tracks/', json={
        'title': 'To Delete',
        'artist': 'Artist',
        'audio_data': audio_data
    })
    track_id = add_res.json['data']['id']
    
    # Delete track
    del_res = test_client.delete(f'/tracks/{track_id}')
    assert del_res.status_code == 204
    assert Track.query.count() == 0

def test_list_tracks(test_client):
    """Test S3: List tracks"""
    # Add two tracks
    test_client.post('/tracks/', json={
        'title': 'Track 1',
        'artist': 'Artist',
        'audio_data': base64.b64encode(b"audio1").decode()
    })
    test_client.post('/tracks/', json={
        'title': 'Track 2',
        'artist': 'Artist',
        'audio_data': base64.b64encode(b"audio2").decode()
    })
    
    response = test_client.get('/tracks/')
    assert response.status_code == 200
    assert len(response.json['data']) == 2
