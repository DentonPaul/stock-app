import os

class BaseConfig:
    STOCK_API_BASE_URL = "https://financialmodelingprep.com/api/v3/"
    STOCK_API_KEY = os.getenv('STOCK_API_KEY', 'demo')

    ## Emailing Errors/Logs ##
    LOG_EMAIL_TOADDRS = ['dp.midfielder7@gmail.com']
    LOG_EMAIL_FROMADDR = "pythonpracticesms@gmail.com"
    LOG_EMAIL_PWD = os.getenv('LOG_EMAIL_PWD', 'demo')  # needs to be defined in current environment
    LOG_EMAIL_SUBJECT = "Error Logs"
    LOG_EMAIL_MAILHOST = ("smtp.gmail.com", 587)
    ## End ##

    ## Timed Rotating Logging ##
    LOG_FILE_PATH = "./stock_app/logs/"
    LOG_ERROR_NAME = "error_file.log"
    LOG_INFO_NAME = "info_file.log"
    LOG_WHEN = "midnight"
    LOG_INTERVAL = 1
    LOG_BACKUP_COUNT = 7 # (one week)
    ## End ##

class DevConfig(BaseConfig):
    EXPLAIN_TEMPLATE_LOADING = True

class ProdConfig(BaseConfig):
    EXPLAIN_TEMPLATE_LOADING = False

class TestConfig(BaseConfig):
    # do NOT put os.environ['FLASK_DEBUG'] = '1'
    pass

connfigurations = {
    'prod': ProdConfig,
    'dev': DevConfig,
    'test': TestConfig
}

