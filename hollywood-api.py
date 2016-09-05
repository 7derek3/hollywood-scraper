from flask import Flask
from flask import jsonify
import psycopg2

app = Flask(__name__)

@app.route('/')
def show_all_dates():
    conn = psycopg2.connect("dbname=hollywood user=derekmiller")
    cur = conn.cursor()

    cur.execute('SELECT * FROM showings;')
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
