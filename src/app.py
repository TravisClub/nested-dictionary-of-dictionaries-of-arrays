from flask import Flask, request, make_response
from functools import wraps

from werkzeug.exceptions import UnsupportedMediaType, BadRequest
from http import HTTPStatus

from src import json_parser


def auth_required(f):
    """Decorator to deal with the basic auth"""

    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'alvaro' and auth.password == '1234':
            return f(*args, **kwargs)

        return make_response('Could not verify your login!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

    return decorated


def create_app():
    application = Flask(__name__)

    @application.route('/')
    @auth_required
    def index():
        return '<h1>You are logged in!</h1>'

    @application.route('/jfile', methods=['POST'])
    @auth_required
    def jfile():
        """
        ---
        post:
          summary: jfile
          description: jfile data endpoint. Performs only basic validation to ensure payloads are legal JSON.
          consumes: [application/json]
          parameters:
            - in: body
              name: jfile
              description: JSON file.
              required: true
              schema:
                type: object
          responses:
            201:
              description: Json was successfully pushed into json_parser.
              content:
                application/json
            400:
              description: Data failed validation and was rejected.
              content:
                application/json
            415:
              description: Payload was not JSON according to content-type header.
              content:
                application/json
            500:
              description: Generic error.
              content:
                application/json
        """
        return handle_posted_data(request, list(request.args))

    return application


def handle_posted_data(request, list_of_args):
    """Handles the control flow of the request.

    Parameters
    ----------
    request : request
        POST request
    list_of_args : list
        request's parameters list

    Returns
    -------
    HTTPStatus : CREATED
        201 code
    """
    payload = validate_json(request)
    json_parser.handle_control_flow(list_of_args, payload)

    return '', HTTPStatus.CREATED


def validate_json(request):
    """Validates the request payload contains a valid JSON.

    Parameters
    ----------
    request : request
        POST request

    Raises
    ------
    *400* `Bad Request`
        Raise if the browser sends something to the application the application
    or server cannot handle.
    *415* `Unsupported Media Type`
        The status code returned if the server is unable to handle the media type
    the client transmitted.

    Returns
    -------
    json_payload : dict
        validated json
    """
    if not request.is_json:
        print("Warning! Bad content-type '{}' in payload".format(request.content_type))
        raise UnsupportedMediaType
    try:
        json_payload = request.get_json()
        return json_payload
    except Exception as e:
        bad_request_error = BadRequest()
        bad_request_error.description = '{}'.format(e)
        raise bad_request_error


if __name__ == '__main__':
    create_app().run()
