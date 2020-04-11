import os

from flask_restplus import Namespace, Resource, fields, Model, representations
from flask import make_response

from BuildForSDG_API.lib import estimator
from flask.helpers import make_response
from flask import g

api = Namespace('on-covid-19', description="Covid 19 related resource")

region = api.model('region', {
    'name': fields.String,
    'avg': fields.Float,
    'avgDailyIncomeInUSD': fields.Float,
    'avgDailyIncomePopulation': fields.Float
})

impact = api.model('impact', {
    'currentlyInfected': fields.Integer,
    'infectionsByRequestedTime': fields.Integer,
    'severeCasesByRequestedTime': fields.Integer,
    'hospitalBedsByRequestedTime': fields.Integer,
    'casesForICUByRequestedTime': fields.Integer,
    'casesForVentilatorsByRequestedTime': fields.Integer,
    'dollarsInFlight': fields.Float
})

data = api.model('data', {
    'region': fields.Nested(region),
    'periodType': fields.String,
    'timeToElapse': fields.Integer,
    'reportedCases': fields.Integer,
    'population': fields.Integer,
    'totalHospitalBeds': fields.Integer
})

estimates = api.model('estimates', {
    'data': fields.Nested(data),
    'impact': fields.Nested(impact),
    'severeImpact': fields.Nested(impact)
})


@api.route('', defaults={'format': 'json'})
@api.route('/<format>')
class OnCovid19(Resource):

    @api.expect(data)
    @api.marshal_with(estimates)
    def post(self, format=None):
        data = api.payload
        return estimator(data)


@api.route('/logs')
class OnCovid19Logs(Resource):
    def get(self):
        with open(os.path.join('requests.log'), 'r') as f:
            logs = f.read()
            return logs
