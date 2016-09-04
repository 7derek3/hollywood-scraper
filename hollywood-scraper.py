from lxml import etree
import psycopg2
from io import StringIO, BytesIO
import requests
import sys
from datetime import datetime

def save_to_db(showings):
    conn = psycopg2.connect("dbname=hollywood user=derekmiller")
    cur = conn.cursor()
    for showing in showings:
        cur.execute('INSERT INTO showings (title, time, url) VALUES (%s, %s, %s)',
                    (showing['title'], showing['time'], showing['url']))
        conn.commit()
    cur.close()
    conn.close()

def getDates():
    today = datetime.today()
    thisMonth = [today.month, today.year]
    def nextMonth(month):
        if month == 12:
            return [month + 1, today.year + 1]
        else:
            return [month + 1, today.year]
    return [thisMonth, nextMonth(today.month)]

def buildUri(month):
    baseUri = 'http://hollywoodtheatre.org/wp-admin/admin-ajax.php?action=aec_ajax&aec_type=widget&aec_widget_id=aec_widget-5-container'
    monthArg = '&aec_month=' + str(month[0])
    yearArg = '&aec_year=' + str(month[1])
    uri = baseUri + monthArg + yearArg
    return uri

def makeRequest(uri):
    page = requests.get(uri)
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(page.text), parser)
    days = tree.xpath('//div[@class=\'aec-event-info\']')
    return days

def parseHtml(days):
    showings = []
    for day in days:
        date = day.xpath('h2[@class=\'widgettitle\']/text()')[0]
        date = date.replace("Showing ", "")
        date = datetime.strptime(date, '%B %d, %Y')
        films = day.xpath('.//li[@class=\'aec-tooltip-feed-agile\']')

        for film in films:
            film_details = film.xpath('.//p')
            film_title_times = film_details[0].xpath('strong/text()')[0]
            film_title_times = film_title_times.split(' |  ')
            url = film_details[1].xpath('a/@href')[0]
            title = film_title_times[0]
            times = film_title_times[1]
            times = times.split()

            for time in times:
                time = datetime.strptime(time, '%I:%M%p')
                time = date.replace(hour=time.hour, minute=time.minute)
                showings.append({'title': title, 'time': time, 'url': url})

    return showings

def main():
    months = getDates()
    thisMonthUri = buildUri(months[0])
    nextMonthUri = buildUri(months[1])
    thisMonthResponse = makeRequest(thisMonthUri)
    nextMonthResponse = makeRequest(nextMonthUri)
    responses = thisMonthResponse + nextMonthResponse
    showings = parseHtml(responses)
    save_to_db(showings)

main()
