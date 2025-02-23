from flask import Blueprint, make_response, jsonify, request
from controller import LookupController


lookup_bp = Blueprint('lookup', __name__)
lookup_controller = LookupController()
@lookup_bp.route('/', methods=['POST'])
def convert_fragment():
    try:
        result, code = lookup_controller.convert_fragment(request.json)
        return make_response(jsonify(result), code)
    except Exception as e:
        print(e)
        return make_response(jsonify({'error': "Internal Server Error"}), 500)
      