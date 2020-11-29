import pytest

from stock_app import create_app

@pytest.fixture
def app():
    return create_app('test')