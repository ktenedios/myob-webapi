from flask_restful import Resource

from app.inversion_of_control import HasMethods, RequiredFeature, features

class FootballSeasonResultsResource(Resource):
    _football_results_parser = RequiredFeature('FootballSeasonResultsParser', HasMethods('get_scores_for_season'))

    def __init__(self):
        pass

    def get(self):
        return self._football_results_parser.get_scores_for_season()

class FootballRoundResultsResource(Resource):
    _football_results_parser = RequiredFeature('FootballRoundResultsParser', HasMethods('get_scores_for_round'))

    def __init__(self):
        pass

    def get(self, round_number):
        return self._football_results_parser.get_scores_for_round(round_number)
