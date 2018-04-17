import requests
from lxml import html

from app.inversion_of_control import (Component, HasMethods, IsInstanceOf,
                                      RequiredFeature)

def ignore_exception(IgnoreException=Exception, DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    Obtained from https://stackoverflow.com/questions/2262333/is-there-a-built-in-or-more-pythonic-way-to-try-to-parse-a-string-to-an-integer
    """
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec

class FootballResultsParser(Component):
    _http_request = RequiredFeature('HttpRequest', HasMethods('get'))
    _http_get_scores_for_round_url_format = RequiredFeature('HttpGetScoresForRoundUrlFormat', IsInstanceOf(str))
    _http_get_scores_for_season_url_format = RequiredFeature('HttpGetScoresForSeasonUrlFormat', IsInstanceOf(str))
    _xpath_get_teams = RequiredFeature('XpathGetTeams', IsInstanceOf(str))
    _xpath_get_scores = RequiredFeature('XpathGetScores', IsInstanceOf(str))
    _xpath_get_match_times = RequiredFeature('XpathGetMatchTimes', IsInstanceOf(str))
    _xpath_get_venues = RequiredFeature('XpathGetVenues', IsInstanceOf(str))

    def __init__(self):
        pass

    def get_scores_for_round(self, round_number):
        url = self._http_get_scores_for_round_url_format.format(round_number)
        html_response = self._http_request.get(url)

        if html_response.status_code == 200:
            return self._get_scores_for_found_page(html_response, round_number)
        else:
            return self._get_error_details_for_not_found_page(html_response, round_number)

    def get_scores_for_season(self):
        url = self._http_get_scores_for_season_url_format
        html_response = self._http_request.get(url)

        if html_response.status_code == 200:
            return self._get_scores_for_found_page(html_response)
        else:
            return self._get_error_details_for_not_found_page(html_response)

    def _get_scores_for_found_page(self, html_response, round_number=''):
        try_parse_int = ignore_exception(ValueError, 'All')(int)
        results_dict = {'round': try_parse_int(round_number)}
        tree = html.fromstring(html_response.content)
        teams = tree.xpath(self._xpath_get_teams)
        scores = tree.xpath(self._xpath_get_scores)
        match_times = tree.xpath(self._xpath_get_match_times)
        venues = tree.xpath(self._xpath_get_venues)
        number_of_teams = len(teams)
        number_of_scores = len(scores)
        number_of_match_times = len(match_times)
        number_of_venues = len(venues)
        error_message = ''

        # The number of teams and the number of scores should match.
        # The number of match times and the number of venues should match.
        # The number of teams should be twice the number of venues.
        if number_of_teams > number_of_scores:
            error_message = 'More teams than scores were identified in urlInvoked'
        elif number_of_teams < number_of_scores:
            error_message = 'More scores than teams were identified in urlInvoked'
        elif number_of_match_times > number_of_venues:
            error_message = 'More match times than venues were identified in urlInvoked'
        elif number_of_match_times < number_of_venues:
            error_message = 'More venues than match times were identified in urlInvoked'
        elif number_of_teams / number_of_venues != 2:
            error_message = 'The number of teams and scores is not double that of the number of match times and venues'

        if len(error_message) > 0:
            return self._get_error_details(round_number, html_response, error_message)

        results_dict['results'] = self._get_results(teams, venues, match_times, scores)

        return results_dict

    def _get_results(self, teams, venues, match_times, scores):
        # There is the possibility that some games do not have scores
        # (e.g. postponed games), so convert non-integer values to None
        try_parse_int = ignore_exception(ValueError, None)(int)

        team_index = 0
        match_time_index = 0
        results = []

        # Teams appear in home team, away team, home team, away team order.
        # Thus scores appear in home score, away score, home score, away score order.
        while team_index < len(teams) - 1:
            result = {
                'venue': venues[match_time_index],
                'timeOfMatch': match_times[match_time_index],
                'homeTeam': teams[team_index],
                'homeScore': try_parse_int(scores[team_index]),
                'awayTeam': teams[team_index + 1],
                'awayScore': try_parse_int(scores[team_index + 1])
            }

            if result['homeScore'] is None or result['awayScore'] is None:
                result['result'] = None
            elif result['homeScore'] > result['awayScore']:
                result['result'] = 'Winner: {0}'.format(result['homeTeam'])
            elif result['homeScore'] < result['awayScore']:
                result['result'] = 'Winner: {0}'.format(result['awayTeam'])
            else:
                result['result'] = 'Draw'

            results.append(result)

            team_index += 2
            match_time_index += 1

        return results

    def _get_error_details(self, round_number, http_response, error_message):
        try_parse_int = ignore_exception(ValueError, 'All')(int)

        return {
            'round': try_parse_int(round_number),
            'urlInvoked': http_response.url,
            'errorMessage': error_message
        }

    def _get_error_details_for_not_found_page(self, html_response, round_number=''):
        try_parse_int = ignore_exception(ValueError, 'All')(int)

        error_dict = {
            'invalidRoundSpecified': try_parse_int(round_number),
            'urlInvoked': html_response.url,
            'httpCode': html_response.status_code
        }

        if html_response.status_code == 404:
            error_dict['errorMessage'] = 'No page exists for round specified'
        else:
            error_dict['errorMessage'] = 'Unexpected error'

        return error_dict
