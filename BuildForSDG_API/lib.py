from functools import wraps


impactCalcs = {
    'CI': lambda x, y: x * y,
    'IBRT': lambda x, y: x * int(2**int(y / 3)),
    'SCBRT': lambda x: int(x * .15),
    'HBBRT': lambda x, y: int((x * .35) - y),
    'CFICUBRT': lambda x: int(x * .05),
    'CFVBRT': lambda x: int(x * .02),
    'DIF': lambda x, y, z, r: round(x * y * z * r, 2)
}


def currentlyInfected(estimator):
    @wraps(estimator)
    def wrapper(data):
        # print(f'currentlyInfected:\n{data}')
        reported_cases = data['data']['reportedCases']
        data.update({
            'impact': {
                'currentlyInfected': impactCalcs['CI'](reported_cases, 10)
            },
            'severeImpact': {
                'currentlyInfected': impactCalcs['CI'](reported_cases, 50)
            }
        })
        return estimator(data)

    return wrapper


def infectionsByRequestedTime(estimator):
    @wraps(estimator)
    def wrapper(data):
        # print(data)
        currently_infected = data['impact']['currentlyInfected']
        currently_infected_severe = data['severeImpact']['currentlyInfected']
        timeToElapse = data['data']['timeToElapse']
        data['impact'].update({
            'infectionsByRequestedTime': impactCalcs['IBRT'](currently_infected, timeToElapse)
        })
        data['severeImpact'].update({
            'infectionsByRequestedTime': impactCalcs['IBRT'](currently_infected_severe, timeToElapse)
        })
        return estimator(data)

    return wrapper


def severeCasesByRequestedTime(estimator):
    @wraps(estimator)
    def wrapper(data):
        infected_by_requested_time = data['impact']['infectionsByRequestedTime']
        infected_by_requested_time_severe = data['severeImpact']['infectionsByRequestedTime']
        data['impact'].update(
            {'severeCasesByRequestedTime': impactCalcs['SCBRT'](infected_by_requested_time)})
        data['severeImpact'].update({'severeCasesByRequestedTime': impactCalcs['SCBRT'](
            infected_by_requested_time_severe)})
        return estimator(data)
    return wrapper


def hospitalBedsByRequestedTime(estimator):
    @wraps(estimator)
    def wrapper(data):

        total_hospital_beds = data['data']['totalHospitalBeds']

        severe_case_by_equested_time = data['impact']['severeCasesByRequestedTime']
        severe_case_by_equested_time_severe = data['severeImpact']['severeCasesByRequestedTime']

        data['impact'].update({
            'hospitalBedsByRequestedTime': impactCalcs['HBBRT'](total_hospital_beds, severe_case_by_equested_time)
        })

        data['severeImpact'].update({
            'hospitalBedsByRequestedTime': impactCalcs['HBBRT'](total_hospital_beds, severe_case_by_equested_time_severe)
        })

        return estimator(data)
    return wrapper


def casesForICUByRequestedTime(estimator):
    @wraps(estimator)
    def wrapper(data):
        infections_by_requested_time = data['impact']['infectionsByRequestedTime']
        infections_by_requested_time_severe = data['severeImpact']['infectionsByRequestedTime']

        data['impact'].update({
            'casesForICUByRequestedTime': impactCalcs['CFICUBRT'](infections_by_requested_time)
        })
        data['severeImpact'].update({
            'casesForICUByRequestedTime': impactCalcs['CFICUBRT'](infections_by_requested_time_severe)
        })

        return estimator(data)
    return wrapper


def casesForVentilatorsByRequestedTime(estimator):
    @wraps(estimator)
    def wrapper(data):
        infections_by_requested_time = data['impact']['infectionsByRequestedTime']
        infections_by_requested_time_severe = data['severeImpact']['infectionsByRequestedTime']

        data['impact'].update({
            'casesForVentilatorsByRequestedTime': impactCalcs['CFVBRT'](infections_by_requested_time)
        })
        data['severeImpact'].update({
            'casesForVentilatorsByRequestedTime': impactCalcs['CFVBRT'](infections_by_requested_time_severe)
        })
        return estimator(data)
    return wrapper


def dollarInFlight(estimator):
    @wraps(estimator)
    def wrapper(data):
        infections_by_requested_time = data['impact']['infectionsByRequestedTime']
        infections_by_requested_time_severe = data['severeImpact']['infectionsByRequestedTime']
        avg_daily_income = data['data']['region']['avgDailyIncomeInUSD']
        avg_daily_income_population = data['data']['region']['avgDailyIncomePopulation']
        timeToElapse = data['data']['timeToElapse']

        impact = {
            'dollarsInFlight': impactCalcs['DIF'](infections_by_requested_time, avg_daily_income, avg_daily_income_population, timeToElapse)
        }
        severeImpact = {
            'dollarsInFlight': impactCalcs['DIF'](infections_by_requested_time_severe, avg_daily_income, avg_daily_income_population, timeToElapse)
        }

        data['impact'] = {**data['impact'], **impact}
        data['severeImpact'] = {**data['severeImpact'], **severeImpact}

        return estimator(data)
    return wrapper


input = {
    "region": {
        "name": "Africa",
        "avgAge": 19.7,
        "avgDailyIncomeInUSD": 4,
        "avgDailyIncomePopulation": 0.73
    },
    "periodType": "days",
    "timeToElapse": 38,
    "reportedCases": 2747,
    "totalHospitalBeds": 678874,
    "population": 92931687
}


def impacts(input):
    def _impacts(estimator):
        @wraps(estimator)
        def wrapper(data):
            input['data'] = data
            return estimator(input)
        return wrapper
    return _impacts


@impacts({})
@currentlyInfected
@infectionsByRequestedTime
@severeCasesByRequestedTime
@hospitalBedsByRequestedTime
@casesForICUByRequestedTime
@casesForVentilatorsByRequestedTime
@dollarInFlight
def estimator(data):
    return data


# @app.before_request
# def start_timer():
#     g, start = time.time()


# @app.after_request
# def log_request(response):
#     if request.path == '/favicon.ico':
#         return response
#     elif request.path.startswith('/static'):
#         return response

#     now = time.time()
#     duration = round(now - g.start, 2)

#     app.logger.info(
#         f'{request.method}\t\t{request.path}\t\t{response.status_code}\t\t{duration}')

#     return response
