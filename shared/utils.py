import hashlib
import logging
import requests
from functools import wraps
from typing import Dict, List, Optional

from flask import current_app, jsonify, request
from werkzeug.exceptions import BadRequest


# --------------------------
# Logging Configuration
# --------------------------

def configure_logging():
    """Initialize standardized logging format"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

configure_logging()
logger = logging.getLogger(__name__)


# --------------------------
# Core Audio Utilities
# --------------------------

def generate_audio_hash(audio_data: bytes) -> str:
    """Generate SHA-256 hash for audio fingerprinting.
    
    Args:
        audio_data: Raw bytes of audio file
        
    Returns:
        Hex digest of SHA-256 hash
    """
    return hashlib.sha256(audio_data).hexdigest()


def validate_audio_format(filename: str, allowed_extensions: List[str] = ['wav']):
    """Validate audio file extension.
    
    Args:
        filename: Uploaded file name
        allowed_extensions: Permitted file types (default: WAV only)
        
    Raises:
        BadRequest: If extension is invalid
    """
    extension = filename.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise BadRequest(f"Invalid file type {extension}. Only WAV files allowed")
    
    
def validate_wav_content(audio_data: bytes):
    """Validate the file is actually a WAV file using header bytes"""
    if len(audio_data) < 44:
        raise BadRequest("Invalid WAV file: File too small")
        
    if not audio_data.startswith(b'RIFF') or audio_data[8:12] != b'WAVE':
        raise BadRequest("Invalid WAV file: Missing RIFF/WAVE headers")


# --------------------------
# API Communication
# --------------------------

def query_audd_api(audio_data: bytes) -> Optional[Dict]:
    """Query Audd.io music recognition API.
    
    Args:
        audio_data: Bytes of audio fragment to identify
        
    Returns:
        Dict with recognition results or None
        
    Raises:
        RuntimeError: For API communication failures
    """
    api_key = current_app.config.get('AUDD_API_KEY')
    
    if not api_key:
        logger.error("Audd.io API key not configured")
        raise RuntimeError("Audio recognition service unavailable")

    try:
        response = requests.post(
            "https://api.audd.io/recognize",
            files={'file': audio_data},
            data={'api_token': api_key},
            timeout=10  # Fail fast
        )
        response.raise_for_status()
        
        result = response.json().get('result')
        if not result:
            logger.warning("No matching track found in Audd.io response")
            return None
            
        return {
            'title': result.get('title'),
            'artist': result.get('artist'),
            'album': result.get('album')
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Audd.io API request failed: {str(e)}")
        raise RuntimeError("Audio recognition service temporary unavailable") from e


# --------------------------
# Response Formatting
# --------------------------

def format_response(data: Optional[Dict] = None, 
                   status: int = 200, 
                   message: str = "success") -> tuple:
    """Standardize API response format.
    
    Args:
        data: Payload to return
        status: HTTP status code
        message: Human-readable message
        
    Returns:
        Tuple of (jsonify response, status code)
    """
    return jsonify({
        'status': status,
        'message': message,
        'data': data
    }), status


# --------------------------
# Error Handling
# --------------------------

class AudioProcessingError(Exception):
    """Custom exception for audio-related failures"""
    pass


def handle_errors(f):
    """Decorator to catch exceptions and return consistent errors"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except BadRequest as e:
            logger.warning(f"Bad request: {str(e)}")
            return format_response(status=400, message=str(e))
        except AudioProcessingError as e:
            logger.error(f"Audio processing failed: {str(e)}")
            return format_response(status=500, message="Audio processing error")
        except Exception as e:
            logger.critical(f"Unexpected error: {str(e)}", exc_info=True)
            return format_response(status=500, message="Internal server error")
    return wrapper


# --------------------------
# Input Validation
# --------------------------

def validate_required_fields(data: Dict, required_fields: List[str]):
    """Validate presence of required fields in request data.
    
    Args:
        data: Request payload
        required_fields: Fields that must be present
        
    Raises:
        BadRequest: If any fields are missing
    """
    missing = [field for field in required_fields if field not in data]
    if missing:
        raise BadRequest(f"Missing required fields: {', '.join(missing)}")


def validate_file_upload(file_key='audio_file', max_size=1000*1024*1024):
    """Validate uploaded WAV file presence, size, and format"""
    if file_key not in request.files:
        raise BadRequest(f"No {file_key} uploaded")
        
    file = request.files[file_key]
    if file.filename == '':
        raise BadRequest("Empty filename")
        
    # Enforce WAV validation at upload time
    validate_audio_format(file.filename)
    
    content = file.read()
    validate_wav_content(content)  # New content validation
    
    if len(content) > max_size:
        raise BadRequest(f"File exceeds {max_size} bytes limit")
        
    file.seek(0)  # Reset file pointer
    return file