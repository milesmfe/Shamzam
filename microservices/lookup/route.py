from flask import Blueprint, make_response, jsonify
from controller import LookupController


lookup_bp = Blueprint('lookup', __name__)
lookup_controller = LookupController()
@lookup_bp.route('/', methods=['GET'])
def index():
    result=lookup_controller.index()
    return make_response(jsonify(data=result))
      