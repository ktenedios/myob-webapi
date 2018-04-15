from app.inversion_of_control import (HasAttributes, HasMethods, IsInstanceOf,
                                      RequiredFeature)

class FootballResultsServer():
    _app = RequiredFeature('Application', HasMethods('run'))
    _api = RequiredFeature('Api', HasMethods('add_resource'))
    _seasonResultsResource = RequiredFeature('SeasonResultsResource', HasAttributes('__name__'))
    _seasonResultsEndpoint = RequiredFeature('SeasonResultsEndpoint', IsInstanceOf(str))
    _roundResultsResource = RequiredFeature('RoundResultsResource', HasAttributes('__name__'))
    _roundResultsEndpoint = RequiredFeature('RoundResultsEndpoint', IsInstanceOf(str))

    def __init__(self):
        self._api.add_resource(self._seasonResultsResource, self._seasonResultsEndpoint)
        self._api.add_resource(self._roundResultsResource, self._roundResultsEndpoint)

    def start(self):
        self._app.run()
