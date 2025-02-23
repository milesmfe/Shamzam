# Shamzam

This project was created to complete the coursework assigned to me under the module, Enterprise Computing (ECM3408), for my final year at The University of Exeter.

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
| D4             | Implement S4 endpoint (POST)     | Not Started |
| D5             | Implement database connection    | Not Started |
| D6             | Develop API layer                | Not Started |
| D7             | Dockerise (Docker)               | Not Started |
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

### Project Structure (Pre-Dockerisation)

Seperate Flask implementations for each microservice, catalogue and lookup. Catalogue satisfies S1, S2 and S3, and lookup satisfies S4. Gateway provides a single entry point for both microservices.

```
.
├── db
│   └── database file
├── microservices
│   ├── catalogue
│   │   └── flask implementation
│   └── lookup
│       └── flask implementation
├── gateway
│   └── flask implementation
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```

## System Design

### Backend

![image](./design/backend.drawio.svg "Backend")

### Catalogue: Add Track

![image](./design/catalogue-add-track.drawio.svg "Catalogue: Add Track")

### Catalogue: Remove Track

![image](./design/catalogue-remove-track.drawio.svg "Catalogue: Remove Track")

### Catalogue: List Tracks

![image](./design/catalogue-list-tracks.drawio.svg "Catalogue: List Tracks")

### Lookup: Convert Fragment

![image](./design/lookup-convert-fragment.drawio.svg "Lookup: Convert Fragment")

## Database Schema

### **Tracks Table**

| Column Name | Data Type | Constraints                           |
| ----------- | --------- | ------------------------------------- |
| id          | INTEGER   | PRIMARY KEY, AUTOINCREMENT            |
| name        | TEXT      | NOT NULL, UNIQUE                      |
| artist      | TEXT      | NOT NULL                              |
| album       | TEXT      | NULLABLE                              |
| genre       | TEXT      | NULLABLE                              |
| duration    | INTEGER   | NOT NULL (seconds)                    |
| file_path   | TEXT      | NOT NULL (location of the music file) |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP             |

### Fragments **Table**

| Column Name | Data Type | Constraints                                |
| ----------- | --------- | ------------------------------------------ |
| id          | INTEGER   | PRIMARY KEY, AUTOINCREMENT                 |
| fragment    | TEXT      | NOT NULL (file path of the fragment)       |
| user_id     | INTEGER   | NULLABLE (if user authentication is added) |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                  |

### Conversions **Table**

| Column Name | Data Type | Constraints                                                              |
| ----------- | --------- | ------------------------------------------------------------------------ |
| id          | INTEGER   | PRIMARY KEY, AUTOINCREMENT                                               |
| fragment_id | INTEGER   | FOREIGN KEY REFERENCES `<span>fragments(id)</span>`, ON DELETE CASCADE |
| track_id    | INTEGER   | FOREIGN KEY REFERENCES `<span>tracks(id)</span>`, ON DELETE CASCADE    |
| confidence  | REAL      | NOT NULL (match confidence score)                                        |
| created_at  | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP                                                |

### SQL

```sql
CREATE TABLE tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    artist TEXT NOT NULL,
    album TEXT,
    genre TEXT,
    duration INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fragments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fragment TEXT NOT NULL,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fragment_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fragment_id) REFERENCES fragments(id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
);
```
