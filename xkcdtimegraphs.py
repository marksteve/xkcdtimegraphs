import base64
import calendar
import json

from flask import (
    Flask,
    abort,
    request,
    render_template,
    url_for,
)
import iso8601
import requests


GH_API_URL = 'https://api.github.com/{}'


app = Flask(__name__)


def to_timestamp(s):
    return calendar.timegm(iso8601.parse_date(s).timetuple())


@app.route('/')
def index():
    return  render_template('index.html')


@app.route('/gh-repo-events', methods=['POST'])
def gh_repo_events():
    url = GH_API_URL.format('repos/{}/events'.format(request.form['repo']))
    r = requests.get(url)
    if r.ok:
        series = dict()
        for event in r.json:
            event_type = event['type'].lower()[:-5]
            if event_type == 'create':
                event_type += '-' + event['payload']['ref_type']
            series.setdefault(event_type, []).append((
                to_timestamp(event['created_at']),
                1,
            ))
        data = []
        for k, v in series.iteritems():
            data.append((
                k,
                v,
            ))
        return url_for(
            'render',
            data=base64.urlsafe_b64encode(json.dumps(data)),
        )
    else:
        abort(500)


@app.route('/render/<data>')
def render(data):
    # data = [
    #   ('series name', [
    #       (12345678, 1.0), (timestamp, value),
    #       (12345678, 2.0),
    #       (12345678, 3.0),
    #    ],
    #   ),
    #   ...
    # ]
    data = json.loads(base64.urlsafe_b64decode(data.encode('utf8')))
    # PROCESS
    import plotter
    return plotter.plot_time_series(data)
    return '[IMAGE HERE]'


if __name__ == '__main__':
    app.run(debug=True)
