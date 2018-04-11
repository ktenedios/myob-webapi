import json
from app.inversion_of_control import Component, HasAttributes, HasMethods, RequiredFeature

class SystemHealthCheck(Component):
    http_request = RequiredFeature('HttpRequest', HasAttributes('status_code') and HasMethods('get'))
    file_reader = RequiredFeature('FileReader', HasMethods('read'))

    def __init__(self, url_to_check):
        self.url_to_check = url_to_check
    
    def check_url(self):
        response = self.http_request.get(self.url_to_check)
        if response.status_code == 200:
            return True, 'URL %s OK' % self.url_to_check
        else:
            return False, 'URL %s did not return HTTP OK' % self.url_to_check

    def get_application_data(self):
        return json.load(self.file_reader)
