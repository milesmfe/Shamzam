# Shamzam

This project was created to complete the coursework assigned to me under the module, Enterprise Computing (ECM3408), for my final year at The University of Exeter.

## Setup & Installation

### Prerequisites

- Python 3.10+
- pip 23.0+
- SQLite (default) or PostgreSQL
- [Audd.io API Key](https://audd.io/)

### 1. Clone Repository

```bash
git clone https://github.com/milesmfe/Shamzam.git
cd shamzam
```

### 2. Install Dependencies

```bash
python -m pip install -r requirements.txt
python -m pip install -e .  # Install project in editable mode
```

### 3. Configure Environment

```bash
echo “AUDD_API_KEY=your_audd_io_key_here” > .env 
echo “FLASK_ENV=development” >> .env
```

## Running Services

### Option 1: Individual Services

```bash
flask --app services.catalogue.app run -p 5000
flask --app services.recognition.app run -p 5001
```

### Option 2: Gateway (All Services)

```bash
gunicorn gateway:application
```

## Specificaiton

### Project Brief

*Shazam is a service that can identify a music tracks from music fragments, provided that the music track is present in the system’s database. The service was launched in the UK as “2580,” the short code that customers dialled on their mobile phone to get a music fragment recognized. Originally, the customer sent a text message containing a music fragment, and was sent back a text message containing music track title and artist name. Later, the service allowed the music track to be downloaded too.*

**Build a Shazam-like MVP called Shamzam using some microservices.**

### Requirements

The following user cases must be satisfied:

* **S1** As an administrator, I want to add a music track to the catalogue, so that a user can listen to it.
* **S2** As an administrator, I want to remove a music track from the catalogue, so that a user cannot listen to it.
* **S3** As an administrator, I want to list the names of the music tracks in the catalogue, so that I know what it contains.
* **S4** As a user, I want to convert a music fragment to a music track in the catalogue, so that I can listen to it.

The following implementation requirements must be satisfied:

1. Python
2. REST API
3. SQLite database
4. Audd.io for audio recognition
5. Unit Testing

## Workflow

| Requirement ID | Description                      | Status      |
| -------------- | -------------------------------- | ----------- |
| P1             | Define project architecture      | Complete    |
| P2             | Set up development environment   | Complete    |
| P3             | Create endpoint diagrams         | Complete    |
| P4             | Design database schemas (SQLite) | Complete    |
| D1             | Implement S1 endpoint (POST)     | Complete    |
| D2             | Implement S2 endpoint (DELETE)   | Complete    |
| D3             | Implement S3 endpoint (GET)      | Complete    |
| D4             | Implement S4 endpoint (POST)     | Complete    |
| D5             | Implement Additional endpoints   | Complete    |
| D6             | Implement database connection    | Complete    |
| D7             | Develop gateway                  | Complete    |
| D8             | Dockerise (Docker)               | Not Started |
| UT1            | Test D1 implementation           | Not Started |
| UT3            | Test D2 implementation          | Not Started |
| UT3            | Test D3 implementation          | Not Started |
| UT4            | Test D4 implementation          | Not Started |
| UT5            | Test D5 implementation           | Not Started |
| E2ET1          | Test happy administrator         | Not Started |
| E2ET2          | Test unhappy administrator      | Not Started |
| E2ET3          | Test happy user                  | Not Started |
| E2ET4          | Test unhappy user               | Not Started |
| DP1            | Deploy & Submit                  | Not Started |

## Architecture

### Stack

* Python ([requirements](requirements.txt))
* Flask
* SQLite
* Audd.io API
* Docker

### Project Structure

Seperate Flask modules for each service, catalogue and recognition. Catalogue satisfies S1, S2 and S3, and recognition satisfies S4. Gateway provides a single entry point for both services.

```
.
├── README.md
├── gateway.py
├── requirements.txt
├── services
│   ├── catalogue
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── extensions.py
│   │   └── test_app.py
│   └── recognition
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── extensions.py
│   │   └── test_app.py
├── setup.py
└── shared
    ├── __init__.py
    └── utils.py
```

## System Design

### Backend

![image](.design/backend.drawio.svg "Backend")

### Catalogue: Add Track

![image](.design/catalogue-add-track.drawio.svg "Catalogue: Add Track")

### Catalogue: Remove Track

![image](.design/catalogue-remove-track.drawio.svg "Catalogue: Remove Track")

### Catalogue: List Tracks

![image](.design/catalogue-list-tracks.drawio.svg "Catalogue: List Tracks")

### Catalogue: Get Track

![Image](.design/catalogue-get-track.drawio.svg "Catalogue: Get Track")

### Recognition: Identify Track

![image](.design/recognition-identify-track.drawio.svg "Recognition: Identify Track")

## Database Schema

### **Table: tracks**

| Column Name | Type         | Description                             | Constraints               |
| ----------- | ------------ | --------------------------------------- | ------------------------- |
| id          | VARCHAR(64)  | SHA-256 hash of audio file content (PK) | PRIMARY KEY               |
| title       | VARCHAR(100) | Song title                              | NOT NULL                  |
| artist      | VARCHAR(100) | Artist name                             | NOT NULL                  |
| audio_file  | BLOB         | Raw audio bytes (MP3/WAV)               | NOT NULL                  |
| created_at  | DATETIME     | Timestamp of addition                   | DEFAULT CURRENT_TIMESTAMP |

### SQLAlchemy

```python
from datetime import datetime
from .extensions import db

class Track(db.Model):
    __tablename__ = 'tracks'
  
    id = db.Column(db.String(64), primary_key=True)  # SHA-256 fingerprint
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    audio_file = db.Column(db.LargeBinary, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "created_at": self.created_at.isoformat()
        }
```
