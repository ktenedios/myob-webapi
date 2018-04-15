import unittest
from app.inversion_of_control import features
from app.system_status import SystemStatus
from tests.mock_application import MockApplication

# Global variables and static methods for validating behaviours
_health_check_method = None
_section_name = None
_section_method = None
_application_for_health_check = None
_path_for_health_check = None
_application_for_environment_dump = None
_path_for_environment_dump = None

def set_global_health_check_method(health_check_method):
    global _health_check_method
    _health_check_method = health_check_method

def set_global_section_properties(section_name, section_method):
    global _section_name
    global _section_method
    _section_name = section_name
    _section_method = section_method

def set_global_application_and_path_for_health_check(application, path):
    global _application_for_health_check
    global _path_for_health_check
    _application_for_health_check = application
    _path_for_health_check = path

def set_global_application_and_path_for_environment_dump(application, path):
    global _application_for_environment_dump
    global _path_for_environment_dump
    _application_for_environment_dump = application
    _path_for_environment_dump = path

class MockHttpRequests():
    def __init__(self):
        self.status_code = 0

    def get(self, url_to_check):
        if url_to_check == 'http://unittesting.com':
            self.status_code = 200
        else:
            self.status_code = 404
        
        # Caller is expecting an object to be returned that contains the attribute status_code
        return self

class MockFileOpen():
    def __init__(self, data_to_return):
        self._data_to_return = data_to_return

    def read(self):
        return self._data_to_return

class MockHealthCheck():
    def __init__(self, app, path):
        set_global_application_and_path_for_health_check(app, path)

    def add_check(self, health_check_method):
        set_global_health_check_method(health_check_method)

class MockEnvironmentDump():
    def __init__(self, app, path):
        set_global_application_and_path_for_environment_dump(app, path)

    def add_section(self, section_name, section_method):
        set_global_section_properties(section_name, section_method)

class TestSystemHealthcheck(unittest.TestCase):
    _mock_file_data = '{"app": {"testcase": "Read JSON file", "author": "Unit Tester", "date": "Wed 10 Jan 2000", "commitsha": "abcd1234"}}'
    _application_section_name = 'Application'
    _application = MockApplication('TestSystemHealthcheck')

    def setUp(self):
        # Allow the dependencies to be replaced so as not to affect unit tests in other test classes
        features.allowReplace = True
        features.Provide('HttpRequest', MockHttpRequests)
        features.Provide('FileReader', MockFileOpen, data_to_return=self._mock_file_data)
        features.Provide('HealthCheck', MockHealthCheck, app=self._application, path='/testHealthCheck')
        features.Provide('EnvironmentDump', MockEnvironmentDump, app=self._application, path='/testEnvironmentDump')
        features.Provide('ApplicationSectionName', self._application_section_name)

    def test_check_url_returns_200_for_valid_page(self):
        url_to_check = 'http://unittesting.com'
        expected_message = 'URL %s OK' % url_to_check
        system_status = SystemStatus(url_to_check)
        result = system_status.check_url()
        self.assertEqual(True, result[0], 'Expecting True to be returned for %s' % url_to_check)
        self.assertEqual(expected_message, result[1], 'Incorrect message returned')

    def test_check_url_does_not_return_200_for_invalid_page(self):
        url_to_check = 'http://invalidpage.com'
        expected_message = 'URL %s did not return HTTP OK' % url_to_check
        system_status = SystemStatus(url_to_check)
        result = system_status.check_url()
        self.assertEqual(False, result[0], 'Expecting False to be returned for %s' % url_to_check)
        self.assertEqual(expected_message, result[1], 'Incorrect message returned')

    def test_get_application_data_contains_app_key(self):
        key = 'app'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(True, key in json_data, 'Expecting %s to have been in json_data' % key)

    def test_get_application_data_does_not_contain_yada_key(self):
        key = 'yada'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(False, key in json_data, 'Expecting %s to not have been in json_data' % key)

    def test_get_application_data_contains_testcase_key_within_app(self):
        key = 'testcase'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Read JSON file', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_author_key_within_app(self):
        key = 'author'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Unit Tester', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_date_key_within_app(self):
        key = 'date'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('Wed 10 Jan 2000', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_contains_commitsha_key_within_app(self):
        key = 'commitsha'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(True, key in json_data['app'], 'Expecting %s to have been in json_data[\'app\']' % key)
        self.assertEqual('abcd1234', json_data['app'][key], 'json_data[\'app\'][\'%s\'] not returning expected string' % key)

    def test_get_application_data_does_not_contain_bla_key_within_app(self):
        key = 'bla'
        system_status = SystemStatus('http://someurl.com')
        json_data = system_status.get_application_data()
        self.assertEqual(False, key in json_data['app'], 'Expecting %s to not have been in json_data[\'app\']' % key)

    def test_health_check_method_added(self):
        system_status = SystemStatus('http://someurl.com')
        self.assertEqual(system_status.check_url, _health_check_method, 'Incorrect health check method')

    def test_environment_dump_method_added(self):
        system_status = SystemStatus('http://someurl.com')
        self.assertEqual(system_status.get_application_data, _section_method, 'Incorrect environment dump method')
        self.assertEqual(self._application_section_name, _section_name, 'Incorrect section name')

    def test_health_check_application_and_path_are_injected(self):
        SystemStatus('http://someurl.com')
        self.assertEqual(self._application, _application_for_health_check, 'The wrong application was injected')
        self.assertEqual('/testHealthCheck', _path_for_health_check, 'The wrong path was injected')

    def test_environment_dump_application_and_path_are_injected(self):
        SystemStatus('http://someurl.com')
        self.assertEqual(self._application, _application_for_environment_dump, 'The wrong application was injected')
        self.assertEqual('/testEnvironmentDump', _path_for_environment_dump, 'The wrong path was injected')
