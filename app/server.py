from app.inversion_of_control import (HasAttributes, HasMethods, IsInstanceOf,
                                      RequiredFeature)

class FootballResultsServer():
    _app = RequiredFeature('Application', HasMethods('run'))
    _api = RequiredFeature('Api', HasMethods('add_resource'))
    _season_results_resource = RequiredFeature('SeasonResultsResource', HasAttributes('__name__'))
    _season_results_endpoint = RequiredFeature('SeasonResultsEndpoint', IsInstanceOf(str))
    _round_results_resource = RequiredFeature('RoundResultsResource', HasAttributes('__name__'))
    _round_results_endpoint = RequiredFeature('RoundResultsEndpoint', IsInstanceOf(str))
    _root_resource = RequiredFeature('RootResource', HasAttributes('__name__'))
    _root_endpoint = RequiredFeature('RootEndpoint', IsInstanceOf(str))
    _system_status = RequiredFeature('SystemStatus')

    def __init__(self):
        self._api.add_resource(self._season_results_resource, self._season_results_endpoint)
        self._api.add_resource(self._round_results_resource, self._round_results_endpoint)
        self._api.add_resource(self._root_resource, self._root_endpoint)

        # Performing this assert as a means of ensuring that system status is instantiated
        assert self._system_status is not None

    def get_application(self):
        return self._app
