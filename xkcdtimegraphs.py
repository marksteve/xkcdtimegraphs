from datetime import datetime
import base64
import calendar
import json
import locale
import os
import time

from flask import (
    Flask,
    abort,
    request,
    render_template,
    url_for,
)
from requests_oauthlib import OAuth1Session
import iso8601
import requests


GH_API_URL = 'https://api.github.com/{}'
TWITTER_API_URL = 'https://api.twitter.com/1.1/{}'


app = Flask(__name__)
twitter = OAuth1Session(
    client_key=os.environ['TWITTER_CLIENT_KEY'],
    client_secret=os.environ['TWITTER_CLIENT_SECRET'],
    resource_owner_key=os.environ['TWITTER_ACCESS_TOKEN'],
    resource_owner_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'],
)


def iso8601_to_timestamp(s):
    return calendar.timegm(iso8601.parse_date(s).timetuple())


def twitter_to_timestamp(s):
    locale.setlocale(locale.LC_TIME, 'C')
    date = datetime(*(time.strptime(s, '%a %b %d %H:%M:%S +0000 %Y')[0:6]))
    locale.setlocale(locale.LC_TIME, '')
    return calendar.timegm(date.timetuple())


@app.route('/')
def index():
    return  render_template('index.html')


@app.route('/gh-repo-events', methods=['POST'])
def gh_repo_events():
    url = GH_API_URL.format('repos/{}/events'.format(request.form['repo']))
    r = requests.get(url)
    if r.ok:
        series = dict()
        for event in r.json():
            event_type = event['type'].lower()[:-5]
            if event_type == 'create':
                event_type += '-' + event['payload']['ref_type']
            series.setdefault(event_type, []).append((
                iso8601_to_timestamp(event['created_at']),
                1,
            ))
        data = []
        for k, v in series.iteritems():
            data.append((k, v))
        return url_for(
            'render',
            data=base64.urlsafe_b64encode(json.dumps(data)),
        )
    else:
        abort(500)


@app.route('/twitter-timeline', methods=['POST'])
def twitter_timeline():
    url = TWITTER_API_URL.format('statuses/user_timeline.json')
    screen_names = [s.strip() for s in request.form['screen_name'].split(',')]
    data = []
    for screen_name in screen_names:
        r = twitter.get(url, params=dict(
            screen_name=screen_name,
            count=100,
        ))
        if r.ok:
            tweets = []
            for tweet in r.json():
                tweets.append((
                    twitter_to_timestamp(tweet['created_at']),
                    1,
                ))
            data.append((screen_name, tweets))
        else:
            abort(500)
    return url_for(
        'render',
        data=base64.urlsafe_b64encode(json.dumps(data)),
    )


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


if __name__ == '__main__':
    app.run(debug=True)
