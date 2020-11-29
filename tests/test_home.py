from flask import url_for

def test_home(client):
    # make a request to our application
    response = client.get('/')
    assert response.status_code == 200
    assert 'Welcome to StockApp' in str(response.data)

def test_lookup(client):
    response = client.post(url_for('home.lookup'), data={'ticker': 'AAPL'})
    assert response.status_code == 302
    assert response.location == url_for('stock.quote', ticker='AAPL', _external=True)
    
