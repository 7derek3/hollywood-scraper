from flask import Flask
import psycopg2

app = Flask(__name__)

@app.route('/')
def show_all_dates():
    conn = psycopg2.connect("dbname=hollywood user=derekmiller")
    cur = conn.cursor()

    cur.execute('SELECT * FROM showings;')
    data = cur.fetchall()
    showings = ''
    for x in data:
        title = x[1]
        time = x[2]
        url = x[3]
        showings += '{}, {}, {}'.format(title, time, url)
    return showings

    cur.close()
    conn.close()
