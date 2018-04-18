from app.inversion_of_control import Component, HasAttributes, HasMethods, RequiredFeature

class SystemStatus(Component):
    _http_request = RequiredFeature('HttpRequest', HasAttributes('status_code') and HasMethods('get'))
    _app_info = RequiredFeature('ApplicationInformation', HasMethods('get_information'))
    _health_check = RequiredFeature('HealthCheck', HasMethods('add_check'))
    _environment_dump = RequiredFeature('EnvironmentDump', HasMethods('add_section'))
    _application_section_name = RequiredFeature('ApplicationSectionName')

    def __init__(self, url_to_check):
        self._url_to_check = url_to_check
        self._health_check.add_check(self.check_url)
        self._environment_dump.add_section(self._application_section_name, self.get_application_data)

    def check_url(self):
        response = self._http_request.get(self._url_to_check)
        if response.status_code == 200:
            return True, 'URL %s OK' % self._url_to_check
        else:
            return False, 'URL %s did not return HTTP OK' % self._url_to_check

    def get_application_data(self):
        return self._app_info.get_information()
