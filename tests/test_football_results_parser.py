import json
import os
import unittest

from app.football_results_parser import FootballResultsParser
from app.inversion_of_control import features

_test_path = os.path.join(os.path.dirname(__file__), 'test_data/test_football_results_parser')

class MockResponse():
    def __init__(self, status_code, content, url):
        self.status_code = status_code
        self.content = content
        self.url = url

class MockHttpFootballRequests():
    _round1_url = 'http://getresults.com?round=1' # Properly formatted HTML with valid data
    _round2_url = 'http://getresults.com?round=2' # Properly formatted HTML with valid data
    _round3_url = 'http://getresults.com?round=3' # Poorly formatted HTML - more teams than scores
    _round4_url = 'http://getresults.com?round=4' # Poorly formatted HTML - more scores than teams
    _round5_url = 'http://getresults.com?round=5' # Poorly formatted HTML - more match times than venues
    _round6_url = 'http://getresults.com?round=6' # Poorly formatted HTML - more venues than match times
    _round7_url = 'http://getresults.com?round=7' # Properly formatted HTML with invalid data - number of teams > number of match times * 2
    _round8_url = 'http://getresults.com?round=8' # Properly formatted HTML with invalid data - number of teams < number of match times * 2
    _non_existent_round_url = 'http://getresults.com?round=9999' # Page does not exist

    def __init__(self):
        pass

    def get(self, url):
        http_status_code = 200

        if url == self._round1_url:
            html_file = os.path.join(_test_path, 'test_football_results_round1.html')
        elif url == self._round2_url:
            html_file = os.path.join(_test_path, 'test_football_results_round2.html')
        elif url == self._round3_url:
            html_file = os.path.join(_test_path, 'more_teams_than_scores.html')
        elif url == self._round4_url:
            html_file = os.path.join(_test_path, 'more_scores_than_teams.html')
        elif url == self._round5_url:
            html_file = os.path.join(_test_path, 'more_match_times_than_venues.html')
        elif url == self._round6_url:
            html_file = os.path.join(_test_path, 'more_venues_than_match_times.html')
        elif url == self._round7_url:
            html_file = os.path.join(_test_path, 'teams_more_than_double_of_venues.html')
        elif url == self._round8_url:
            html_file = os.path.join(_test_path, 'teams_less_than_double_of_venues.html')
        else:
            http_status_code = 404
            html_file = os.path.join(_test_path, 'file_not_found.html')

        # Using the with statement to open the file, otherwise the tests
        # will report 'ResurceWarning: unclosed file'
        with open(file=html_file, mode='r') as f:
            return MockResponse(http_status_code, f.read(), url)

class TestFootballResults(unittest.TestCase):
    def setUp(self):
        # Allow the dependencies to be replaced so as not to affect unit tests in other test classes
        features.allowReplace = True
        features.Provide('HttpRequest', MockHttpFootballRequests)
        features.Provide('HttpGetScoresUrlFormat', 'http://getresults.com?round={0}')
        features.Provide('XpathGetTeams', '//div[@class="teamname"]/text()')
        features.Provide('XpathGetScores', '//div[@class="score"]/text()')
        features.Provide('XpathGetMatchTimes', '//div[@class="matchtime"]/text()')
        features.Provide('XpathGetVenues', '//div[@class="venuename"]/text()')

    def _compare_expected_and_actual_round_results(self, round_number, expecting_error_output=False):
        # When comparing dictionaries, allow unit tests to display entire contents
        self.maxDiff = None

        if round_number in [1, 2] and not expecting_error_output:
            expected_data_file = os.path.join(_test_path, 'expected_round{0}_results.json'.format(round_number))
        elif round_number in [3, 4, 5, 6, 7, 8] and expecting_error_output:
            expected_data_file = os.path.join(_test_path, 'expected_parsing_error_round{0}.json'.format(round_number))
        else:
            expected_data_file = os.path.join(_test_path, 'expected_non_existent_round_results.json')

        # Using the with statement to open the file, otherwise the tests
        # will report 'ResurceWarning: unclosed file'
        with open(file=expected_data_file, mode='r') as file_reader:
            expected_data = json.load(file_reader)
            football_results_parser = FootballResultsParser()
            actual_data = football_results_parser.get_scores_for_round(round_number)

            self.assertIsNotNone(actual_data, 'An instantiated object should have been returned')
            self.assertIsInstance(actual_data, dict, 'A dictionary object should have been returned')
            self.assertDictEqual(expected_data, actual_data, 'The retrieved dictionary does not match with expected dictionary')

    def test_get_scores_for_round_1(self):
        self._compare_expected_and_actual_round_results(1)

    def test_get_scores_for_round_2(self):
        self._compare_expected_and_actual_round_results(2)

    def test_get_scores_for_non_existent_round(self):
        self._compare_expected_and_actual_round_results(9999)

    def test_get_scores_returns_error_when_more_teams_than_scores(self):
        self._compare_expected_and_actual_round_results(round_number=3, expecting_error_output=True)

    def test_get_scores_returns_error_when_more_scores_than_teams(self):
        self._compare_expected_and_actual_round_results(round_number=4, expecting_error_output=True)

    def test_get_scores_returns_error_when_more_match_times_than_venues(self):
        self._compare_expected_and_actual_round_results(round_number=5, expecting_error_output=True)

    def test_get_scores_returns_error_when_more_venues_than_match_times(self):
        self._compare_expected_and_actual_round_results(round_number=6, expecting_error_output=True)

    def test_get_scores_returns_error_when_number_of_teams_is_more_than_double_number_of_venues(self):
        self._compare_expected_and_actual_round_results(round_number=7, expecting_error_output=True)

    def test_get_scores_returns_error_when_number_of_teams_is_less_than_double_number_of_venues(self):
        self._compare_expected_and_actual_round_results(round_number=8, expecting_error_output=True)
