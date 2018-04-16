import unittest

from flask_restful import Resource
from tests.mock_application import MockApplication

from app.inversion_of_control import features
from app.server import FootballResultsServer

# Global variables for recording whether FootballResultsServer called
# the constructor and the add_resource method of the dependency-injected Api object
_resources = None
_application = None

class MockApi():
    def __init__(self, application):
        global _application
        global _resources
        _application = application
        _resources = []

    def add_resource(self, resource_class, endpoint):
        _resources.append({
            'resourceClass': resource_class.__name__,
            'endpoint': endpoint
        })

class MockFootballSeasonResultsResource(Resource):
    def __init__(self):
        pass

    def get(self):
        return {'className': __name__}

class MockFootballRoundResultsResource(Resource):
    def __init__(self):
        pass

    def get(self, round_number):
        return {'className': __name__, 'roundNumber': round_number}

class TestFootballResultsServer(unittest.TestCase):
    _expected_application_name = 'mock_app_name'
    _application = None

    def setUp(self):
        self._application = MockApplication(self._expected_application_name)

        # Allow the dependencies to be replaced so as not to affect unit tests in other test classes
        features.allowReplace = True

        # A lambda expression is used to return the application instance to the requestor.
        # This is consistent with what has been implemented in ../app/wsgi.py.
        features.Provide('Application', lambda: self._application)
        features.Provide('Api', MockApi, application=self._application)
        features.Provide('SeasonResultsResource', lambda: MockFootballSeasonResultsResource)
        features.Provide('SeasonResultsEndpoint', '/season')
        features.Provide('RoundResultsResource', lambda: MockFootballRoundResultsResource)
        features.Provide('RoundResultsEndpoint', '/round/<round_number>')

    def test_server_adds_injected_resources(self):
        # Expected state of resources held by instance of FootballResultsServer
        expected_resources = [
            {
                'resourceClass': MockFootballRoundResultsResource.__name__,
                'endpoint': '/round/<round_number>'
            },
            {
                'resourceClass': MockFootballSeasonResultsResource.__name__,
                'endpoint': '/season'
            }
        ]

        # Pre-test verification
        self.assertIsNone(_resources, 'No resources should be present as FootballResultsServer was not instantiated')
        
        FootballResultsServer()
        
        # Verify setup after initialization of FootballResultsServer instance
        self.assertEqual(len(expected_resources), len(_resources), \
            'The number of resoureces set by FootballResultsServer does not match with what is expected')

        # The two lists consist of dictionaries, with the ordering of elements being different.
        # Hence this loop evaluates that both lists have the same dictionary contents.
        for expected in expected_resources:
            for expected_key in expected.keys():
                expected_value = expected[expected_key]
                resource_exists_in_actual = False

                for actual in _resources:
                    if expected_key in actual.keys() and expected_value == actual[expected_key]:
                        resource_exists_in_actual = True

                self.assertTrue(resource_exists_in_actual, \
                    'Resources set by FootballResultsServer is missing \'{0}\': \'{1}\''.format(expected_key, expected_value))

    def test_server_calls_application_run_method(self):
        server = FootballResultsServer()
        server.start()
        self.assertTrue(self._application.get_run_invoked(), \
            'The start method of FootballResultsServer should have called the run method belonging to the injected application')
