from flask import Blueprint, render_template, current_app
import requests

# API_URL = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}'

stock = Blueprint('stock', __name__)

def fetch_price(ticker):
    url = '{}/stock/real-time-price/{}'.format(current_app.config['STOCK_API_BASE_URL'], ticker.upper())
    data = requests.get(url, params={'apikey': current_app.config['STOCK_API_KEY']}).json()
    return data['price']

def fetch_income(ticker):
    url = '{}financials/income-statement/{}'.format(current_app.config['STOCK_API_BASE_URL'], ticker.upper())
    financials = requests.get(url, params={'apikey': current_app.config['STOCK_API_KEY']}).json()["financials"]
    financials.sort(key=lambda quarter: quarter["date"])
    return financials

@stock.route('/<string:ticker>')
def quote(ticker):
    price = fetch_price(ticker)
    return render_template('stock/quote.html', ticker=ticker, stock_price=price)

@stock.route('/<string:ticker>/financials')
def financials(ticker):
    financials = fetch_income(ticker)

    chart_data = [float(q["EPS"]) for q in financials if q["EPS"]]
    chart_params = {"type": 'line',
                    "data": {
                        'labels': [q["date"] for q in financials if q["EPS"]],
                        'datasets': [{'label': 'EPS', 'data': chart_data}]
                    }}
    return render_template('stock/financials.html', ticker=ticker, financials=financials, 
                            chart_params=chart_params)
