import os

class BaseConfig:
    STOCK_API_BASE_URL = "https://financialmodelingprep.com/api/v3/"
    STOCK_API_KEY = os.getenv('STOCK_API_KEY', 'demo')

class DevConfig(BaseConfig):
    EXPLAIN_TEMPLATE_LOADING = True

class ProdConfig(BaseConfig):
    # STOCK_API_KEY = 'prodkey'
    STOCK_API_KEY = os.getenv('STOCK_API_KEY', 'demo')

class TestConfig(BaseConfig):
    pass

connfigurations = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig
}

