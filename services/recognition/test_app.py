import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch, MagicMock

import requests
from services.recognition.app import create_app

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_health(client: FlaskClient):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode() == 'Recognition operational'

def test_index(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data

@patch('services.recognition.app.validate_file_upload')
@patch('services.recognition.app.validate_audio_format')
@patch('services.recognition.app.requests.post')
@patch('services.recognition.app.requests.get')
def test_recognize_success(mock_get, mock_post, mock_validate_format, mock_validate_upload, client: FlaskClient):
    mock_file = MagicMock()
    mock_file.filename = 'test.wav'
    mock_file.read.return_value = b'audio data'
    mock_validate_upload.return_value = mock_file

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        'result': {
            'title': 'Test Title',
            'artist': 'Test Artist'
        }
    }

    mock_get.side_effect = [
        MagicMock(status_code=200, json=lambda: {'data': [{'id': '123'}]}),
        MagicMock(status_code=200, json=lambda: {'data': {'id': '123', 'title': 'Test Title', 'artist': 'Test Artist'}})
    ]

    response = client.post('/api/recognize', data={'audio_file': (mock_file, 'test.wav')})
    assert response.status_code == 200
    assert response.json == {'id': '123', 'title': 'Test Title', 'artist': 'Test Artist'}

@patch('services.recognition.app.validate_file_upload')
@patch('services.recognition.app.validate_audio_format')
@patch('services.recognition.app.requests.post')
@patch('services.recognition.app.requests.get')
def test_recognize_no_match(mock_get, mock_post, mock_validate_format, mock_validate_upload, client: FlaskClient):
    mock_file = MagicMock()
    mock_file.filename = 'test.wav'
    mock_file.read.return_value = b'audio data'
    mock_validate_upload.return_value = mock_file

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {'result': None}

    response = client.post('/api/recognize', data={'audio_file': (mock_file, 'test.wav')})
    assert response.status_code == 404
    assert response.json == {
        "error": "No matching track found in recognition service",
        "code": "NO_RECOGNITION_MATCH"
    }

@patch('services.recognition.app.validate_file_upload')
@patch('services.recognition.app.validate_audio_format')
@patch('services.recognition.app.requests.post')
@patch('services.recognition.app.requests.get')
def test_recognize_catalogue_error(mock_get, mock_post, mock_validate_format, mock_validate_upload, client: FlaskClient):
    mock_file = MagicMock()
    mock_file.filename = 'test.wav'
    mock_file.read.return_value = b'audio data'
    mock_validate_upload.return_value = mock_file

    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {
        'result': {
            'title': 'Test Title',
            'artist': 'Test Artist'
        }
    }

    mock_get.return_value.status_code = 500

    response = client.post('/api/recognize', data={'audio_file': (mock_file, 'test.wav')})
    assert response.status_code == 502
    assert response.json == {
        "error": "Catalogue service unavailable",
        "code": "CATALOGUE_ERROR"
    }

@patch('services.recognition.app.validate_file_upload')
@patch('services.recognition.app.validate_audio_format')
@patch('services.recognition.app.requests.post')
@patch('services.recognition.app.requests.get')
def test_recognize_timeout(mock_get, mock_post, mock_validate_format, mock_validate_upload, client: FlaskClient):
    mock_file = MagicMock()
    mock_file.filename = 'test.wav'
    mock_file.read.return_value = b'audio data'
    mock_validate_upload.return_value = mock_file

    mock_post.side_effect = requests.exceptions.Timeout

    response = client.post('/api/recognize', data={'audio_file': (mock_file, 'test.wav')})
    assert response.status_code == 504
    assert response.json == {
        "error": "Request to external service timed out",
        "code": "TIMEOUT_ERROR"
    }
