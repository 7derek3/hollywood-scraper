from lxml import etree
from io import StringIO, BytesIO
import requests
import sys
from datetime import datetime, timedelta
import datetime as dt
import argparse
import calendar

class Showing(object):
    def __init__(self, title, time):
        self.title = title
        self.time = time

def getDates(dateRange):
    today = datetime.today()
    thisMonth = [today.month, today.year]
    if dateRange == "today" or "this" in dateRange:
        return [thisMonth]
    def nextMonth(month):
        if month == 12:
            return [month + 1, today.year + 1]
        else:
            return [month + 1, today.year]
    return [thisMonth, nextMonth(today.month)]

def parseLimit(limit):
    today = datetime.today()
    if limit == "today":
        return [today,today]
    if "this" in limit:
        if "week" in limit:
            # return today.week
            day_of_week = today.weekday()
            to_end_of_week = dt.timedelta(days=6 - day_of_week)
            end_of_week = today + to_end_of_week
            return [today,end_of_week]
        if "month" in limit:
            return [today,datetime(today.year, today.month, calendar.mdays[today.month])]
    if "next" in limit:
        if "week" in limit:
            # return today.week
            week_from_now = today + dt.timedelta(days=7)
            day_of_week = week_from_now.weekday()
            #get the start of next week
            to_beginning_of_week = dt.timedelta(days=day_of_week)
            beginning_of_week = week_from_now - to_beginning_of_week
            #get the end of next week
            to_end_of_week = dt.timedelta(days=6 - day_of_week)
            end_of_week = week_from_now + to_end_of_week
            return [beginning_of_week,end_of_week]
        if "month" in limit:
            end_of_this_month = datetime(today.year, today.month, calendar.mdays[today.month])
            end_of_next_month = datetime(today.year, today.month+1, calendar.mdays[today.month+1])
            return [end_of_this_month,end_of_next_month]

    return
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

def parseHtml(days, limit):
    for day in days:
        date = day.xpath('h2[@class=\'widgettitle\']/text()')[0]
        date = date.replace("Showing ", "")
        date = datetime.strptime(date, '%B %d, %Y')
        films = day.xpath('.//li[@class=\'aec-tooltip-feed-agile\']')

        for film in films:
            film = film.xpath('p/strong/text()')[0]
            film = film.split(' |  ')
            title = film[0]
            times = film[1]
            times = times.split()

            for time in times:
                time = datetime.strptime(time, '%I:%M%p')
                time = date.replace(hour=time.hour, minute=time.minute)
                showing = Showing(title, time)
                date_limit = parseLimit(limit)
                if showing.time.date() >= date_limit[0].date() and showing.time.date() <= date_limit[1].date():
                    print (showing.title, showing.time.strftime('%X %x %Z'))

def main():
        hollywood_logo = """\ Hollywood D
    #   #     ##     #      #      #   #  #    ###   #    ##     ##    #####
    #   #    #  #    #      #       # #   #    # #   #   #  #   #  #   #    #
    #####   #    #   #      #        #     #   # #   #  #    # #    #  #    #
    #   #    #  #    #      #        #     #  #  #  #    #  #   #  #   #    #
    #   #     ##     ####   ####     #      ##    ##      ##     ##    #####
    """
    print(hollywood_logo)
    parser = argparse.ArgumentParser(description='Movie Times!')
    parser.add_argument('when',type=str,nargs='+',help='Time range for showings from today (e.g. Today, This Week)')
    args = parser.parse_args()
    datelimit =  "".join(args.when).lower()
    months = getDates(datelimit)
    responses = ""
    for month in months:
        MonthUri = buildUri(month)
        responses = makeRequest(MonthUri)
    output = parseHtml(responses,datelimit)

main()
