from unittest.mock import patch

from flask import Flask
from flask_restful import Api, Resource
from flask_testing import TestCase

from app.inversion_of_control import features
from app.server import FootballResultsServer

# Variable (effectively a constant) for validating that the system status instance
# is registered with the required URL to be checked
_expected_url_to_check = 'https://system-status.com'

# Global variables and functions to be used for API and health endpoint testing.
# These are in place in a bid to prevent the following error when running multiple tests:
# AssertionError: View function mapping is overwriting an existing endpoint function: mockfootballseasonresultsresource
_server = None
_application = None
_injected_system_status = None

def get_server():
    global _server

    if _server is None:
        _server = FootballResultsServer()

    return _server

def get_application(test_case):
    global _application

    if _application is None:
        _application = Flask(__name__)
        _application.config['TESTING'] = True

        # The OS will pick the port that the application runs on.
        # This avoids two instances on the same machine trying to use the same port.
        _application.config['LIVESERVER_PORT'] = 0

        # A lambda expression is used to return the application instance to the requestor.
        # This is consistent with what has been implemented in ../app/wsgi.py.
        features.Provide('Application', lambda: _application)
        features.Provide('Api', Api, app=_application)
        features.Provide('SeasonResultsResource', lambda: MockFootballSeasonResultsResource)
        features.Provide('SeasonResultsEndpoint', '/season')
        features.Provide('RoundResultsResource', lambda: MockFootballRoundResultsResource)
        features.Provide('RoundResultsEndpoint', '/round/<round_number>')
        features.Provide('SystemStatus', MockSystemStatus, _expected_url_to_check),
        features.Provide('RootResource', lambda: MockRootEndpointResource)
        features.Provide('RootEndpoint', '/')

    return _application

def set_injected_system_status(system_status):
    global _injected_system_status
    _injected_system_status = system_status

class MockFootballSeasonResultsResource(Resource):
    def __init__(self):
        pass

    def get(self):
        return {'className': self.__class__.__name__}

class MockFootballRoundResultsResource(Resource):
    def __init__(self):
        pass

    def get(self, round_number):
        return {'className': self.__class__.__name__, 'roundNumber': int(round_number)}

class MockRootEndpointResource(Resource):
    def __init__(self):
        pass

    def get(self):
        return {'mockingRootEndpoint': 'true'}

class MockSystemStatus(Resource):
    def __init__(self, url_to_check):
        self._url_to_check = url_to_check
        set_injected_system_status(self)

    def get_url_to_check(self):
        return self._url_to_check

class TestFootballResultsServer(TestCase):
    _application = None

    def create_app(self):
        self._application = get_application(self)
        return self._application

    def setUp(self):
        pass

    @patch('flask.Flask')
    def test_get_application_returns_expected_flask_application(self, mock_flask):
        server = get_server()
        flask_application = server.get_application()

        # Validate that the application returned by the get_application method is the Flask application that was set up
        self.assertEqual(self._application, flask_application, 'The get_application method returned the wrong Flask application instance')

    def test_system_status_injected_into_server(self):
        get_server()
        self.assertIsNotNone(_injected_system_status, 'A system status instance should have been injected into FootballResultsServer')
        self.assertIsInstance(_injected_system_status, MockSystemStatus, 'Incorrect object type injected')

        actual_url_to_check = _injected_system_status.get_url_to_check()
        self.assertIsNotNone(actual_url_to_check, 'No URL was injected into the constructor of system status')
        self.assertEqual(_expected_url_to_check, actual_url_to_check, 'The wrong URL was injected into the constructor of system status')

    def test_season_endpoint_returns_expected_data(self):
        get_server()
        expected_dict = dict(className='MockFootballSeasonResultsResource')
        response = self.client.get('/season')
        self.assert200(response, 'HTTP 200 should have been returned for the season endpoint')
        self.assertDictEqual(expected_dict, response.json, 'The retrieved dictionary does not match with what was expected')

    def test_round_endpoint_returns_expected_data_with_round_number(self):
        get_server()

        for round_number in 1, 2, 3:
            expected_dict = dict(className='MockFootballRoundResultsResource', roundNumber=round_number)
            response = self.client.get('/round/{0}'.format(round_number))
            self.assert200(response, 'HTTP 200 should have been returned for the round endpoint')
            self.assertDictEqual(expected_dict, response.json, 'The retrieved dictionary does not match with what was expected')
