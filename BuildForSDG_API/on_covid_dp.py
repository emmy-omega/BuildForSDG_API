from flask import Blueprint, request, Response
from simplexml.core import dumps
from BuildForSDG_API.lib import estimator

bp = Blueprint('on-covid-19', __name__,
               url_prefix='/api/v1/on-covid-19')


@bp.route('', methods=['POST'])
@bp.route('/json', methods=['POST'])
def index():
    data = request.json
    estimates = estimator(data)
    return estimates


@bp.route('/xml', methods=['POST'])
def xml():
    data = request.json
    estimates = estimator(data)
    xml_estimates = dumps({'root': estimates})
    return Response(xml_estimates, 200, mimetype='application/xml')


@bp.route('/logs')
def logs():
    with open('requests.log', 'r') as f:
        _logs = f.read()
        return Response(_logs, 200, mimetype='text/plain')
