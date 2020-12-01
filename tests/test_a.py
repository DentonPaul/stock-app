'''SET FLASK_DEBUG = 0 for tests to work correctly'''
import os

def test_set_flask_debug(client):
    os.environ['FLASK_DEBUG'] = '1'

