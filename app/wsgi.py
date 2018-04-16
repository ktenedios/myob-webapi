import os

import requests
from flask import Flask
from flask_restful import Api
from healthcheck import EnvironmentDump, HealthCheck

from app.football_results_parser import FootballResultsParser
from app.football_results_resource import (FootballRoundResultsResource,
                                           FootballSeasonResultsResource)
from app.inversion_of_control import features
from app.server import FootballResultsServer

if __name__ == '__main__':
    # Application data file used for environment dump REST endpoint
    app_data_file = os.path.join(os.path.dirname(__file__), 'application_information.json')

    # Create Flask object for hosting the application.
    # Note that a lambda expression is used for returning the application instance,
    # otherwise classes such as FootballResultServer will not be able to use the object.
    application = Flask('FootballResultsApi')
    features.Provide('Application', lambda: application)

    # Dependencies for parsing football results from a HTML page
    features.Provide('HttpRequest', requests)
    features.Provide('HttpGetScoresForRoundUrlFormat', 'http://websites.sportstg.com/comp_info.cgi?a=ROUND&round={0}&client=0-10178-0-478257-0&pool=1')
    features.Provide('HttpGetScoresForSeasonUrlFormat', 'http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=-1&client=0-10178-0-435486-0&pool=1')
    features.Provide('XpathGetTeams', '//a[@class="teamnames"]/text()')
    features.Provide('XpathGetScores', '//div[@class="big-score"]/text()')
    features.Provide('XpathGetMatchTimes', '//div[@class="match-time"]/text()')
    features.Provide('XpathGetVenues', '//a[@class="venuename"]/text()')

    # Dependencies required by the resources that expose RESTful endpoints for obtaining scores
    features.Provide('FootballSeasonResultsParser', FootballResultsParser)
    features.Provide('FootballRoundResultsParser', FootballResultsParser)

    # Dependencies required for running the RESTful server.
    # Note that lambda expressions are used for returning the required class type for a resource.
    features.Provide('Api', Api, app=application)
    features.Provide('SeasonResultsResource', lambda: FootballSeasonResultsResource)
    features.Provide('SeasonResultsEndpoint', '/season')
    features.Provide('RoundResultsResource', lambda: FootballRoundResultsResource)
    features.Provide('RoundResultsEndpoint', '/round/<round_number>')

    # Dependencies required for reporting on health status and providing a system dump
    features.Provide('FileReader', open, file=app_data_file, mode='r')
    features.Provide('HealthCheck', HealthCheck, app=application, path='/healthCheck')
    features.Provide('EnvironmentDump', EnvironmentDump, app=application, path='/environmentDump')
    features.Provide('ApplicationSectionName', 'FootballResultsApi')

    # Moment of truth - instantiate the server and run the application
    server = FootballResultsServer()
    server.start()
