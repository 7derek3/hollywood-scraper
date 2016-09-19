from flask import Flask
from flask import jsonify, redirect, request
from flask_cors import CORS
import os
from urllib.parse import urlparse
import psycopg2
import datetime

app = Flask(__name__)
CORS(app)

@app.route('/showings')
def get_showings():
    # Logic for setting start_date and end_date
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if not start_date and not end_date:
        start_date = datetime.datetime.today()
        end_date = start_date + datetime.timedelta(days=7)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    elif not start_date and end_date:
        start_date = datetime.datetime.today()
        start_date = start_date.strftime('%Y-%m-%d')
    elif start_date and not end_date:
        end_date = start_date
    try:
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        end_date = datetime.datetime.combine(end_date, datetime.time(23, 59, 59))
    except ValueError:
        return jsonify({'errors': {'status': '400', 'details': \
                        'Incorrect date format. Should be \'year-month-day\''}})

    sql = 'SELECT * FROM showings WHERE time BETWEEN \'{}\' AND \'{}\' \
                 ORDER BY time ASC;'.format(start_date, end_date)

    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()

    # Output response to desired json
    showings = {}
    titles = {}
    for x in data:
        _id = x[0]
        title = x[1]
        _datetime = x[2]
        url = x[3]

        date = _datetime.strftime('%Y-%m-%d')
        time = _datetime.strftime('%H:%M')

        if date not in showings:
            showings[date] = []
            if titles:
                showings[last_date].append(titles)
                titles = {}
        if title not in titles:
            titles[title] = {}
            titles[title]['url'] = url
            titles[title]['showtimes'] = []
        if time not in titles[title]['showtimes']:
            titles[title]['showtimes'].append(time)
            last_date = date

    showings[last_date].append(titles)
    cur.close()
    conn.close()

    return jsonify(showings)

@app.route('/new')
def new_showings():
    max_number = request.args.get('max_number')

    if not max_number:
        max_number = 5

    sql = 'SELECT DISTINCT title, MAX(url), MAX(id) FROM showings \
           GROUP BY title ORDER BY MAX(id) DESC LIMIT %s;' % max_number
    conn = open_db_connection()
    cur = conn.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    showings = []
    for x in data:
        _id = x[2]
        title = x[0]
        url = x[1]
        showings.append({'title': title, 'url': url})
    cur.close()
    conn.close()

    return jsonify(showings)

def open_db_connection():
    url = urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )

    return conn
