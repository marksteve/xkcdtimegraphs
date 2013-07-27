from flask import Flask, render_template


GTRENDS_URL = "http://www.google.com/trends/fetchComponent?q=%s&cid=TIMESERIES_GRAPH_0&export=3"


app = Flask(__name__)


@app.route('/')
def index():
    return  render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
