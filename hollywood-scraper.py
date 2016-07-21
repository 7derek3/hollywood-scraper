from lxml import etree
from io import StringIO, BytesIO
import requests
import sys
from datetime import datetime

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
        print(date.strftime('%B %d, %Y'))
        films = day.xpath('.//li[@class=\'aec-tooltip-feed-agile\']')

        for film in films:
            print(film.xpath('p/strong/text()')[0])

def main():
    uri = buildUri(7, 2016)
    days = makeRequest(uri)
    output = parseHtml(days)

main()
