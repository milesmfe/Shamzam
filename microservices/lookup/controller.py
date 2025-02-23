class LookupController:
    def convert_fragment(self, request):
        required_fields = {'fragment'}
        
        # Check request
        if not request: return {'error': 'Missing required fields'}, 400
        if not all(field in request for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        # TODO: Check if fragment is valid
        
        # TODO: Audd.io API connection: Convert fragment to music
        
        # TODO: Database connection: Check if music exists in database
        
        # TODO: Database connection: Get music from database
        full_track = {'name': 'Name', 'artist': 'Artist', 'album': 'Album', 'genre': 'Genre', 'duration': 0}
        track_id = 0
        
        return {'full_track': full_track, 'track_id': track_id}, 200
