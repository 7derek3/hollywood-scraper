from flask import Flask
from flask import jsonify
from flask import request
import os
import urlparse
import psycopg2
import datetime

app = Flask(__name__)

@app.route('/')
def get_showings():
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])

    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    cur = conn.cursor()

    start_date = request.headers.get('start_date')
    end_date = request.headers.get('end_date')

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

    cur.execute('SELECT * FROM showings WHERE time BETWEEN %s AND %s \
                 ORDER BY time ASC;', (start_date, end_date))
    data = cur.fetchall()
    showings = []
    for x in data:
        _id = x[0]
        title = x[1]
        time = x[2]
        url = x[3]
        showings.append({'id': _id, 'title': title, 'time': time, 'url': url})
    return jsonify(showings)

    cur.close()
    conn.close()
