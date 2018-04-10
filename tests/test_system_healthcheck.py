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

class TestSystemHealthcheck(unittest.TestCase):

    def setUp(self):
        if not 'HttpRequest' in features.providers:
            features.Provide('HttpRequest', MockHttpRequests)
    
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
    
if __name__ == '__main__':
    unittest.main()
