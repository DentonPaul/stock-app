import os

# make testing environment = development
def test_set_env():
    os.environ['FLASK_ENV'] = 'development'