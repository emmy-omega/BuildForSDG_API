import os
import time
from logging import basicConfig, DEBUG, getLogger
from logging.config import dictConfig


import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from flask import Flask, Blueprint, request, g

from api.v1 import api, bp

# Config logging
# basicConfig(filename='requests.log', filemode='a',
#             level=DEBUG)

dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        },
        'file': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'requests.log',
            'formatter': 'file'
        }
    },
    'loggers': {
        'BuildForSDG_API': {
            'level': 'DEBUG',
            'handlers': ['file']
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


def create_app(test_config=None):
    app = Flask(__name__.split('.')[0], instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=b'<\x1c\xf6-\t\xb1\xe4\x17\x87!\xf4\xfeO\xe2\xac_',
        DATABASE=os.path.join(app.instance_path, 'BuildForSDG.sqlite')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError as err:
        # app.logger.error(err)
        pass

    @app.before_request
    def start_timer():
        g.start = time.time()
        # app.logger.debug(g.start)

    @app.after_request
    def log_request(response):
        if request.path == '/favicon.ico':
            return response
        elif request.path.startswith('/static'):
            return response

        # get logger
        log = getLogger(__name__.split('.')[0])

        now = time.time()
        duration = round(now - g.start, 2)
        app.logger.debug(duration)
        log.debug(
            f'{request.method}\t\t{request.path}\t\t{response.status_code}\t\t{duration} ms')

        return response

    app.register_blueprint(bp, url_prefix='/api/v1')

    # api.init_app(app)

    return app
