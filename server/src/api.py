from flask import Blueprint, jsonify

blueprint = Blueprint('api', __name__, url_prefix='/api')


@blueprint.route('/submissions', methods=['GET'])
def list_submissions():
    # TODO: implement
    return jsonify('')
