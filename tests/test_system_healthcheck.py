import unittest
from app.inversion_of_control import features
from app.system_healthcheck import SystemHealthCheck

class MockHttpRequests():
    status_code = 0

    def __init__(self):
        pass
    
    def get(self, url_to_check):
        if url_to_check == 'http://unittesting.com':
            self.status_code = 200
        else:
            self.status_code = 404
        
        # Caller is expecting an object to be returned that contains the attribute status_code
        return self

class MockFileOpen():
    def __init__(self, data_to_return):
        self.data_to_return = data_to_return

    def read(self):
        return self.data_to_return

class TestSystemHealthcheck(unittest.TestCase):
    mock_file_data = '{"app": {"testcase": "Read JSON file", "author": "Unit Tester", "date": "Wed 10 Jan 2000", "commitsha": "abcd1234"}}'

    def setUp(self):
        if not 'HttpRequest' in features.providers:
            features.Provide('HttpRequest', MockHttpRequests)

        if not 'FileReader' in features.providers:
            features.Provide('FileReader', MockFileOpen, data_to_return=self.mock_file_data)

    def test_check_url_returns_200_for_valid_page(self):
        url_to_check = 'http://unittesting.com'
        expected_message = 'URL %s OK' % url_to_check
        health_check = SystemHealthCheck(url_to_check)
        result = health_check.check_url()
        self.assertEqual(True, result[0], 'Expecting True to be returned for %s' % url_to_check)
        self.assertEqual(expected_message, result[1], 'Incorrect message returned')

    def test_check_url_does_not_return_200_for_invalid_page(self):
        url_to_check = 'http://invalidpage.com'
        expected_message = 'URL %s did not return HTTP OK' % url_to_check
        health_check = SystemHealthCheck(url_to_check)
        result = health_check.check_url()
        self.assertEqual(False, result[0], 'Expecting False to be returned for %s' % url_to_check)
        self.assertEqual(expected_message, result[1], 'Incorrect message returned')

    def test_get_application_data_contains_app_key(self):
        key = 'app'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(True, key in json_data, 'Expecting %s to have been in json_data' % key)

    def test_get_application_data_does_not_contain_yada_key(self):
        key = 'yada'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(False, key in json_data, 'Expecting %s to not have been in json_data' % key)

    def test_get_application_data_contains_testcase_key_within_app(self):
        key = 'testcase'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Read JSON file', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_author_key_within_app(self):
        key = 'author'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Unit Tester', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_date_key_within_app(self):
        key = 'date'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Wed 10 Jan 2000', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_commitsha_key_within_app(self):
        key = 'commitsha'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('abcd1234', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_does_not_contain_bla_key_within_app(self):
        key = 'bla'
        health_check = SystemHealthCheck('http://someurl.com')
        json_data = health_check.get_application_data()
        self.assertEqual(False, key in json_data['app'], 'Expecting %s to not have been in json_data[\'app\']' % key)

if __name__ == '__main__':
    unittest.main()
