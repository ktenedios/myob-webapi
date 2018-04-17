from app.inversion_of_control import (HasAttributes, HasMethods, IsInstanceOf,
                                      RequiredFeature)

class FootballResultsServer():
    _app = RequiredFeature('Application', HasMethods('run'))
    _api = RequiredFeature('Api', HasMethods('add_resource'))
    _season_results_resource = RequiredFeature('SeasonResultsResource', HasAttributes('__name__'))
    _season_results_endpoint = RequiredFeature('SeasonResultsEndpoint', IsInstanceOf(str))
    _round_results_resource = RequiredFeature('RoundResultsResource', HasAttributes('__name__'))
    _round_results_endpoint = RequiredFeature('RoundResultsEndpoint', IsInstanceOf(str))
    _system_status = RequiredFeature('SystemStatus')

    def __init__(self):
        self._api.add_resource(self._season_results_resource, self._season_results_endpoint)
        self._api.add_resource(self._round_results_resource, self._round_results_endpoint)

        # Performing this assert as a means of ensuring that system status is instantiated
        assert self._system_status is not None

    def start(self):
        self._app.run()
