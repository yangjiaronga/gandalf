# coding=utf-8
import os

from flask import Blueprint, jsonify, make_response, request

from .main import main
from .rqlib import q

api = Blueprint('api', __name__)


@api.app_errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method Not Allowed'}), 405)


@api.app_errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@api.app_errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@api.route('/hooks', methods=['POST', 'GET'])
def index():
    data = request.json
    event = request.headers.get('X-Github-Event')

    # open
    if not (event == 'pull_request' and data['action'] == 'opened'):
        return jsonify({'error': 'Only support pull request open event'})

    pr_url = data['pull_request']['html_url']
    ticket_id = data['number']
    from_sha = data['pull_request']['head']['sha']
    repo_name = data['pull_request']['head']['repo']['full_name']
    fork_from = data['pull_request']['base']['repo']['full_name']
    q.enqueue(main, fork_from, from_sha, repo_name, ticket_id,
              pr_url)
    return jsonify({'ok': 1})
