from flask import Blueprint, make_response, jsonify, request
from controller import CatalogueController


catalogue_bp = Blueprint('catalogue', __name__)
catalogue_controller = CatalogueController()
    
@catalogue_bp.route('/tracks/add', methods=['POST'])
def add_track():
  result = catalogue_controller.add_track(request.json)
  return make_response(jsonify(result))