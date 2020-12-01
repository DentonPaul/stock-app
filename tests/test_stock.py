from flask import url_for
import requests
import pytest

class MockPrice:
    @staticmethod
    def json():
        return {'price': 42, 'ticker': 'AAPL'}

class MockFinancials:
    @staticmethod
    def json():
        return {'financials': [{'date': '2019-01-01', 'Revenue': '100.00', 
                                'Gross Margin': '0.383','Revenue Growth': '0.1', 'EPS': '2.2'}]}

class MockNotFound:
    @staticmethod
    def json():
        return {}

def test_quote(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockPrice

    monkeypatch.setattr(requests, 'get', mock_get)

    response = client.get(url_for('stock.quote', ticker='AAPL'))
    assert response.status_code == 200
    assert b'Price: $42' in response.data
    assert b'AAPL' in response.data

def test_financials(client, monkeypatch):
    def mock_get(*args, **kwargs):
        return MockFinancials

    monkeypatch.setattr(requests, 'get', mock_get)

    response = client.get(url_for('stock.financials', ticker='AAPL'))
    assert response.status_code == 200
    assert b'quickchart.io/chart' in response.data
    assert b'2019-01-01' in response.data
    assert b'38.3%' in response.data
    assert b'$100' in response.data

## FLASK_ENV=development for tests to run properly ## 

def test_invalid_quote(client, monkeypatch):
    def mock_empty_response(*args, **kwargs):
        return MockNotFound
    monkeypatch.setattr(requests, 'get', mock_empty_response)

    with pytest.raises(KeyError):
        client.get(url_for('stock.quote', ticker='NOTFOUND'))

def test_invalid_empty_ticker(client, monkeypatch):
    def mock_empty_response(*args, **kwargs):
        return MockNotFound
    monkeypatch.setattr(requests, 'get', mock_empty_response)

    response = client.get(url_for('stock.quote', ticker='ticker').replace('ticker', ''))
    assert response.status_code == 404
