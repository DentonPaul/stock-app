from flask import Blueprint, render_template, current_app
from stock_app.stock_data import fetch_price, fetch_income

stock = Blueprint('stock', __name__)

@stock.route('/<string:ticker>')
def quote(ticker):
    price = fetch_price(ticker, current_app.config)
    return render_template('stock/quote.html', ticker=ticker, stock_price=price)

@stock.route('/<string:ticker>/financials')
def financials(ticker):
    financials = fetch_income(ticker, current_app.config)

    chart_data = [float(q["EPS"]) for q in financials if q["EPS"]]
    chart_params = {"type": 'line',
                    "data": {
                        'labels': [q["date"] for q in financials if q["EPS"]],
                        'datasets': [{'label': 'EPS', 'data': chart_data}]
                    }}
    return render_template('stock/financials.html', ticker=ticker, financials=financials, 
                            chart_params=chart_params)
