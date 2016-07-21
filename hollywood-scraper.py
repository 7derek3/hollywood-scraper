from lxml import etree
from io import StringIO, BytesIO
import requests
import sys
from datetime import datetime

def buildUri(month, year):
    baseUri = 'http://hollywoodtheatre.org/wp-admin/admin-ajax.php?action=aec_ajax&aec_type=widget&aec_widget_id=aec_widget-5-container'
    monthUri = '&aec_month=' + str(month)
    yearUri = '&aec_year=' + str(year)
    uri = baseUri + monthUri + yearUri
    return uri

page = requests.get(buildUri(7, 2016))
parser = etree.HTMLParser()
tree = etree.parse(StringIO(page.text), parser)
days = tree.xpath('//div[@class=\'aec-event-info\']')

for day in days:
    date = day.xpath('h2[@class=\'widgettitle\']/text()')[0]
    date = date.replace("Showing ", "")
    date = datetime.strptime(date, '%B %d, %Y')
    print(date.strftime('%B %d, %Y'))
    films = day.xpath('.//li[@class=\'aec-tooltip-feed-agile\']')

    for film in films:
        print(film.xpath('p/strong/text()')[0])
