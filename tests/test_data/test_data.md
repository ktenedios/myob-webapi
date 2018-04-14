# Test data
This folder consists of test data to be used by the unit tests.

For each Python test file that requires test data (e.g. `../test_football_results_parser.py`), a folder of the same name as the test class (e.g. `test_football_results_parser`) will exist in this folder and will contain the required test data files.

This document will outline each test case requiring test data, and how this test data is used.

## test_football_results_parser
As the class `FootballResultsParser` parses HTML content and returns JSON content to the caller, the test data consists of various HTML content, and expected JSON data to be returned.

The HTML content is retrieved using a mock class that represents the `requests` class based on the URL that is supplied to it.
