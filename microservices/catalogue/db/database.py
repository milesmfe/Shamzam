import sqlite3
import os

CREATE_TRACKS_TABLE = '''
CREATE TABLE IF NOT EXISTS tracks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    artist TEXT NOT NULL,
    album TEXT,
    genre TEXT,
    duration INTEGER NOT NULL,
    file_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''

CREATE_FRAGMENTS_TABLE = '''
CREATE TABLE IF NOT EXISTS fragments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fragment TEXT NOT NULL,
    user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
'''
CREATE_CONVERSIONS_TABLE = '''
CREATE TABLE IF NOT EXISTS conversions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fragment_id INTEGER NOT NULL,
    track_id INTEGER NOT NULL,
    confidence REAL NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fragment_id) REFERENCES fragments(id) ON DELETE CASCADE,
    FOREIGN KEY (track_id) REFERENCES tracks(id) ON DELETE CASCADE
)
'''

def create_database():
    if not os.path.exists('microservices/catalogue/db/catalogue.db'):
        open('microservices/catalogue/db/catalogue.db', 'w').close()
    conn = sqlite3.connect('microservices/catalogue/db/catalogue.db')
    c = conn.cursor()
    c.execute(CREATE_TRACKS_TABLE)
    c.execute(CREATE_FRAGMENTS_TABLE)
    c.execute(CREATE_CONVERSIONS_TABLE)
    conn.commit()
    conn.close()