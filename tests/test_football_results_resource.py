import json
import unittest

from app.football_results_resource import (FootballRoundResultsResource,
                                           FootballSeasonResultsResource)
from app.inversion_of_control import features

_expected_json_for_season_results = '{"roundNumber": "All", "methodCalled": "get_scores_for_season"}'
_expected_json_for_round_results = '{"roundNumber": ROUND_NUMBER, "methodCalled": "get_scores_for_round"}'

class MockFootballResultsParser():
    def __init__(self):
        pass

    def get_scores_for_round(self, round_number):
        return json.loads(_expected_json_for_round_results.replace('ROUND_NUMBER', str(round_number)))

    def get_scores_for_season(self):
        return json.loads(_expected_json_for_season_results)

class TestFootballResultsResource(unittest.TestCase):
    def setUp(self):
        # Allow the dependencies to be replaced so as not to affect unit tests in other test classes
        features.allowReplace = True
        features.Provide('FootballSeasonResultsParser', MockFootballResultsParser)
        features.Provide('FootballRoundResultsParser', MockFootballResultsParser)

    def test_get_season_results(self):
        resource = FootballSeasonResultsResource()
        expected_dict = json.loads(_expected_json_for_season_results)
        get_result = resource.get()
        self.assertDictEqual(expected_dict, get_result, 'JSON returned by get method of FootballSeasonResultsResource is incorrect')

    def test_get_round_results(self):
        resource = FootballRoundResultsResource()
        round_number = 1

        while round_number <= 3:
            expected_dict = json.loads(_expected_json_for_round_results.replace('ROUND_NUMBER', str(round_number)))
            get_result = resource.get(round_number)

            self.assertDictEqual(expected_dict, get_result, \
                'JSON returned by get method of FootballRoundResultsResource for round {0} is incorrect'.format(round_number))

            round_number += 1
