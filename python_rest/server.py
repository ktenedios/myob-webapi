from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
from flask.ext.jsonpify import jsonpify
from lxml import html
import requests

# http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=1&client=0-10178-0-478257-0&pool=1
# http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=2&client=0-10178-0-478257-0&pool=1
# http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=3&client=0-10178-0-478257-0&pool=1
# http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=4&client=0-10178-0-478257-0&pool=1

# page = requests.get('http://websites.sportstg.com/comp_info.cgi?a=ROUND&round=1&client=0-10178-0-478257-0&pool=1')
# tree = html.fromstring(page.content)
# teams = tree.xpath('//a[@class="teamnames"]/text()')
# scores = tree.xpath('//div[@class="big-score"]/text()')

# x = 0
# while x < len(teams) - 1:
#     print(teams[x] + ' ' + scores[x] + ', ' + teams[x + 1] + ' ' + scores[x + 1])
#     x += 2

# match_times = tree.xpath('//div[@class="match-time"]/text()')
# print(match_times)
# ['8:15\xa0PM / Thu\xa022 Feb', '7:30\xa0PM / Fri\xa023 Feb', '8:30\xa0PM / Fri\xa023 Feb', '6:00\xa0PM / Sat\xa024 Feb', '7:00\xa0PM / Sat\xa024 Feb', '8:30\xa0PM / Mon\xa026 Feb', '8:30\xa0PM / Mon\xa026 Feb']
# for x in range(0, len(match_times)):
#     print(match_times[x].replace('\xa0', ' '))

# match_venues = tree.xpath('//a[@class="venuename"]/text()')
# print(match_venues)
# ['Kingston Heath Soccer Complex - Pitch 1', 'Knights Stadium - Pitch 1', 'Green Gully Reserve - Pitch 1', 'JL Murphy Reserve - SS Anderson Oval - Pitch 1', 'Hosken Reserve - Pitch 1', 'The Grange Reserve', 'Veneto Club - David Barro Stadium (S)']

# class 