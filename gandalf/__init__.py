# coding=utf-8
import os

from flask import Flask

from gandalf.api import api

__version__ = '0.3'


def create_app():
    app = Flask(__name__)
    token = os.getenv('GITHUB_AUTH_TOKEN')
    if token is None:
        raise EnvironmentError(
            'Environment Variable $GITHUB_AUTH_TOKEN must be set '
            'to use the github reporter.')
    app.config['GITHUB_AUTH_TOKEN'] = token
    app.register_blueprint(api, url_prefix='/api')
    return app
