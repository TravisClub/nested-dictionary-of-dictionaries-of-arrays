import pytest
import base64


@pytest.fixture
def app():
    from src import app
    api_app = app.create_app()
    api_app.debug = True
    api_app.testing = True

    yield api_app


def test_jfile_endpoint_rejects_http_get_requests(app):
    api_client = app.test_client()
    response = api_client.get('/jfile')
    assert response.status_code == 405


def test_jfile_endpoint_rejects_http_get_requests_with_allow_header_in_response(app):
    api_client = app.test_client()
    response = api_client.get('/jfile')
    assert 'Allow' in response.headers


def test_index_does_basic_auth(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro:1234").decode()
    res = api_client.get("/", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert res.status_code == 200


def test_index_gives_back_unauthorized_when_wrong_user_or_password(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro1:1234").decode()
    res = api_client.get("/", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert res.status_code == 401


def test_jfile_gives_back_unauthorized_when_wrong_user_or_password(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro1:1234").decode()
    res = api_client.post("/jfile", headers={"Authorization": "Basic {}".format(user_credentials)})
    assert res.status_code == 401


def test_jfile_returns_201_created_when_valid_payload_and_parameters_in_request(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro:1234").decode()
    res = api_client.post("/jfile?city",
                          data='[{"country": "US","city": "Boston","currency": "USD","amount": 100},{"country": "FR","city": "Paris","currency": "EUR","amount": 20}]',
                          headers={'content-type': 'application/json',
                                   "Authorization": "Basic {}".format(user_credentials)})
    assert res.status_code == 201


def test_jfile_endpoint_rejects_non_json_content_typ_415_unsupported_media_type(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro:1234").decode()
    response = api_client.post('/jfile',
                               data='<xml><thing></thing></xml>',
                               headers={'content-type': 'application/xml',
                                        "Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 415


def test_jfile_endpoint_rejects_invalid_json_request_payload_with_400_bad_request(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro:1234").decode()
    response = api_client.post('/jfile?city',
                               data='{"json": "with no closing brace"',
                               headers={'content-type': 'application/json',
                                        "Authorization": "Basic {}".format(user_credentials)})
    assert response.status_code == 400


def test_jfile_endpoint_returns_no_entity_body_on_happy_path(app):
    api_client = app.test_client()
    user_credentials = base64.b64encode(b"alvaro:1234").decode()
    response = api_client.post('/jfile?thing', data='[{"thing": "blah"}]', headers={'content-type': 'application/json',
                                                                                    "Authorization": "Basic {}".format(
                                                                                        user_credentials)})
    assert len(response.data) == 0

