from flask import Flask
import requests

app = Flask(__name__)

API_URL = 'https://financialmodelingprep.com/api/v3/stock/real-time-price/{ticker}'

def fetch_price(ticker):
    data = requests.get(API_URL.format(ticker=ticker.upper()), params={'apikey':'demo'}).json()
    return data['price']

# http:/localhost:5000/stock/AAPL

@app.route('/stock/<ticker>')
def stock(ticker):
    price = fetch_price(ticker)
    return "The price of the {ticker} is {price}".format(ticker=ticker, price=price)

@app.route('/')
def home():
    return "Try /stock/AAPL aye hello me"
    
