import time
import redis

from flask import Flask, request, url_for, redirect, render_template

app = Flask(__name__, template_folder='web')
cache = redis.Redis(host='redis', port=6379)
app.static_folder = 'web'

def get_hit_count():
    retries = 5
    while True:
        try:
            return  cache.incr('hits')
        except redis.exception.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/map')
def map():
    return render_template("map.html")

@app.route('/api/v1/pilon', methods=['GET'])
def hello():
    count = get_hit_count()
    return  'Helo World! I have been seen {} times.\n'.format(count)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)