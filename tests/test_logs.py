from flask import url_for

def test_logs(client):
    response = client.get(url_for('home.logs_status'))
    assert response.status_code == 200
    