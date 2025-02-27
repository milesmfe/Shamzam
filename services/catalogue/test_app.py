from io import BytesIO
import pytest
from services.catalogue.app import create_app, db
from services.catalogue.track import Track

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_health(client):
    response = client.get('/tracks/health')
    assert response.status_code == 200
    assert response.data == b'Catalogue operational'

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Main catalogue interface' in response.data

def test_add_track(client):
    data = {
        'title': 'Test Title',
        'artist': 'Test Artist'
    }
    audio_file = (BytesIO(b"fake audio data"), 'test.wav')
    response = client.post('/tracks', data=data, content_type='multipart/form-data')
    assert response.status_code == 201
    assert b'Track added successfully' in response.data

def test_remove_track(client):
    track = Track(id='test_id', title='Test Title', artist='Test Artist', audio_file=b'fake audio data')
    db.session.add(track)
    db.session.commit()

    response = client.delete(f'/tracks/{track.id}')
    assert response.status_code == 204

def test_list_tracks(client):
    track = Track(id='test_id', title='Test Title', artist='Test Artist', audio_file=b'fake audio data')
    db.session.add(track)
    db.session.commit()

    response = client.get('/tracks/')
    assert response.status_code == 200
    assert b'Track details retrieved' in response.data

def test_get_track(client):
    track = Track(id='test_id', title='Test Title', artist='Test Artist', audio_file=b'fake audio data')
    db.session.add(track)
    db.session.commit()

    response = client.get(f'/tracks/{track.id}')
    assert response.status_code == 200
    assert b'Track details retrieved' in response.data

def test_search_tracks(client):
    track = Track(id='test_id', title='Test Title', artist='Test Artist', audio_file=b'fake audio data')
    db.session.add(track)
    db.session.commit()

    response = client.get('/tracks/search?title=Test')
    assert response.status_code == 200
    assert b'Search results' in response.data
