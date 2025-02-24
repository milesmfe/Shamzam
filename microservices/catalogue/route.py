from flask import Blueprint, make_response, jsonify, request
from microservices.catalogue.controller import CatalogueController


catalogue_bp = Blueprint('catalogue', __name__)
catalogue_controller = CatalogueController()
    
@catalogue_bp.route('/tracks/add', methods=['POST'])
def add_track():
  try:
    result, code = catalogue_controller.add_track(request.json)
    return make_response(jsonify(result), code)
  except Exception as e:
    print(e)
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)
  
@catalogue_bp.route('/tracks/<id>', methods=['GET'])
def get_track(id):
  try:
    result, code = catalogue_controller.get_track(id)
    return make_response(jsonify(result), code)
  except Exception as e:
    print(e)
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)
  
@catalogue_bp.route('/tracks/<id>', methods=['DELETE'])
def remove_track(id):
  try:
    result, code = catalogue_controller.remove_track(id)
    return make_response(jsonify(result), code)
  except Exception as e:
    print(e)
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)
  
@catalogue_bp.route('/tracks/list', methods=['GET'])
def list_tracks():
  try:
    result, code = catalogue_controller.list_tracks()
    return make_response(jsonify(result), code)
  except Exception as e:
    print(e)
    return make_response(jsonify({'error': 'Internal Server Error'}), 500)