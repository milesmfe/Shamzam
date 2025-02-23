class CatalogueController:
    def add_track(self, request):
        required_fields = {'name', 'artist', 'album', 'genre', 'duration'}
        
        # Check request
        if not request: return {'error': 'Missing required fields'}, 400
        if not all(field in request for field in required_fields):
            return {'error': 'Missing required fields'}, 400
        
        # TODO: Database connection: Insert track into database
        track_id = 0
        
        return {'message': 'Track added successfully', 'track_id': track_id}, 201
    
    def remove_track(self, id):
        
        # Check id
        if not id: return {'error': 'Track not specified'}, 400
        if not id.isdigit(): return {'error': 'Invalid track id'}, 400
        
        # TODO: Check if track exists in database
        
        # TODO: Database connection: Remove track from database
        return {'message': 'Track removed successfully'}, 200
    
    def list_tracks(self):
        # TODO: Database connection: Get all tracks from database
        tracks = [{'id': i, 'name': f'Track {i}', 'artist': f'Artist {i}', 'album': f'Album {i}', f'genre': f'Genre {i}', 'duration': i*100} for i in range(5)]
        
        return {'tracks': tracks}, 200