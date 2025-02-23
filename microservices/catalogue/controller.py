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