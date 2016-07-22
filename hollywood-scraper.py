from lxml import etree
from io import StringIO, BytesIO
import requests
import sys
import re
from datetime import datetime

class Showing(object):

    def __init__(self, name, date):
        self.name = name
        self.date = date

def getDate():
    today = datetime.today()
    month = today.month
    year = today.year
    return month, year

def buildUri(month, year):
    baseUri = 'http://hollywoodtheatre.org/wp-admin/admin-ajax.php?action=aec_ajax&aec_type=widget&aec_widget_id=aec_widget-5-container'
    monthArg = '&aec_month=' + str(month)
    yearArg = '&aec_year=' + str(year)
    uri = baseUri + monthArg + yearArg
    return uri

def makeRequest(uri):
    page = requests.get(uri)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(page.text), parser)
    days = tree.xpath('//div[@class=\'aec-event-info\']')
    return days

def parseHtml(days):
    for day in days:
        date = day.xpath('h2[@class=\'widgettitle\']/text()')[0]
        date = date.replace("Showing ", "")
        date = datetime.strptime(date, '%B %d, %Y')
        # print(date.strftime('%B %d, %Y'))
        films = day.xpath('.//li[@class=\'aec-tooltip-feed-agile\']')

        for film in films:
            titleTimes = film.xpath('p/strong/text()')[0]

            title = re.search('(.*) \|', titleTimes)
            title = title.group(1)
            print title

            times = re.search('\|  (.*)', titleTimes)
            times = times.group(1)
            print times


def main():
    month, year = getDate()
    uri = buildUri(month, year)
    days = makeRequest(uri)
    output = parseHtml(days)

main()
