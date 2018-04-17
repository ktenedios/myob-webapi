from flask_restful import Resource

from app.inversion_of_control import HasMethods, RequiredFeature, features

class FootballSeasonResultsResource(Resource):
    _football_results_parser = RequiredFeature('FootballSeasonResultsParser', HasMethods('get_scores_for_season'))
    _pretty_json_renderer = RequiredFeature('PrettyJson')

    def __init__(self):
        pass

    def get(self):
        return self._pretty_json_renderer(self._football_results_parser.get_scores_for_season())

class FootballRoundResultsResource(Resource):
    _football_results_parser = RequiredFeature('FootballRoundResultsParser', HasMethods('get_scores_for_round'))
    _pretty_json_renderer = RequiredFeature('PrettyJson')

    def __init__(self):
        pass

    def get(self, round_number):
        return self._pretty_json_renderer(self._football_results_parser.get_scores_for_round(round_number))

class RootEndpointResource(Resource):
    _pretty_json_renderer = RequiredFeature('PrettyJson')

    def __init__(self):
        pass

    def get(self):
        app_doc = {
            'application' : 'NPL Victoria 2018 Football Results',
            'purpose' : 'RESTful API for obtaining football results of the NPL Victoria 2018 competition',
            'endpoints' : [
                {
                    'endpoint' : '/',
                    'purpose' : 'Gets a description of the application (this document)'
                },
                {
                    'endpoint' : '/season',
                    'purpose' : 'Get entire 2018 season results'
                },
                {
                    'endpoint' : '/round/<round_number>',
                    'purpose' : 'Get the results for a specified round'
                },
                {
                    'endpoint' : '/healthCheck',
                    'purpose' : 'Get results of a system health check'
                },
                {
                    'endpoint' : '/environmentDump',
                    'purpose' : 'Gets a dump of the environment this application is running from, including application details'
                }
            ]
        }

        return self._pretty_json_renderer(app_doc)
