from services.catalogue.extensions import db

class Track(db.Model):
    """Database model for music tracks"""
    __tablename__ = 'tracks'
    
    id = db.Column(db.String(64), primary_key=True)  # SHA-256 hash
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    audio_file = db.Column(db.LargeBinary, nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist
        }