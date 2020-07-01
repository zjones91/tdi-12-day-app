from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components


def getdata(ticker):
    requrl = "https://www.quandl.com/api/v3/datasets/WIKI/" + ticker + ".json?start_date=2018-01-01&end_date=2019-01-01&order=asc&column_index=4&collapse=quarterly&transformation=rdiff" + '&api_key=ZNPPXjNQduDUh64S3RRk'
    r = requests.get(requrl)

    return_data = r.json()['dataset']
    df = pd.DataFrame(return_data['data'], columns=return_data['column_names'])
    df.columns = [col.lower() for col in df.columns]
    df = df.set_index(pd.DatetimeIndex(df['date']))
    return df


def getplot(df, priceTypes, ticker):
    p = figure(title="Quandl WIKI EOD Stock Prices - 2018", x_axis_type="datetime", x_axis_label="Date",
               y_axis_label="Stock price", plot_width=1000)

    mapping = {'open': 'open', 'adjOpen': 'adj. open', 'close': 'close', 'adjClose': 'adj. close'}
    color = {'open': 'orange', 'adjOpen': 'red', 'close': 'blue', 'adjClose': 'green'}

    for priceType in priceTypes:
        p.line(df.index, df[mapping[priceType]], color=colour[priceType], legend=ticker + ": " + mapping[priceType])
    return p


app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/plots')


@app.route('/plots', methods=['GET', 'POST'])
def index():
    return render_template('plots.html')


@app.route('/graphs', methods=['GET', 'POST'])
def graph():
    ticker = request.form['ticker']
    ticker = ticker.upper()
    priceTypes = request.form.getlist('priceType')

    data = getdata(ticker)
    plot = getplot(data, priceTypes, ticker)

    script, div = components(plot)
    requrl = "https://www.google.com/finance?q=" + ticker
    return render_template('graphs.html', script=script, div=div, reqUrl=requrl)


if __name__ == '__main__':
    app.run(port=33507)