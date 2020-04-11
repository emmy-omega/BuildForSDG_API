from flask_restplus import Api, Resource
from flask import Blueprint, make_response
from simplexml.core import dumps, element_from_dict

from .covid19_ns import api as covid_ns

bp = Blueprint('api', __name__)

api = Api(bp, title='BuildForSDG API', version='1.0.0')

api.add_namespace(covid_ns)


@api.representation('application/xml')
def output_xml(data, code, headers=None):

    dumped = dumps({'output': data})

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp


@api.representation("text/plain")
def output_hmtl(data, code, headers=None):
    resp = make_response(data, code)
    resp.headers.extend(headers or {})
    return resp
