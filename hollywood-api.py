from flask import Flask
from flask import jsonify
import psycopg2
import datetime

app = Flask(__name__)

@app.route('/')
def get_showings(start_date='', end_date=''):
    conn = psycopg2.connect("dbname=hollywood user=derekmiller")
    cur = conn.cursor()
    if start_date == '' and end_date == '':
        start_date = datetime.datetime.today()
        end_date = start_date + datetime.timedelta(days=7)
        start_date = start_date.strftime('%Y-%m-%d')
        end_date = end_date.strftime('%Y-%m-%d')
    elif end_date == '':
        end_date == start_date

    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')

    cur.execute('SELECT * FROM showings WHERE time BETWEEN %s AND %s;', (start_date, end_date))
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
