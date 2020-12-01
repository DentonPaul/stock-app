from logging.config import dictConfig
from flask import current_app

class LogSetup(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs) # pragma: no cover

    def init_app(self, app):
        debug = app.debug # if app is in debug mode (bool)

        std_formatters = {
            "formatters": {
                "default": {
                    "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
                },
                "access": {
                    "format": "%(message)s",
                }
            }
        }

        std_handlers = {
            "handlers": {
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "email": {
                    "class": "logging.handlers.SMTPHandler",
                    "formatter": "default",
                    "level": "INFO", # change this to WARNING
                    "mailhost": ("smtp.gmail.com", 587),
                    "fromaddr": "pythonpracticesms@gmail.com",
                    "toaddrs": ["2483285403@vzwpix.com"],
                    "subject": "Error Logs",
                    "credentials": ("pythonpracticesms@gmail.com", "thisisapassword"), # put this in config
                },
                "error_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "default",
                    "filename": "./stock_app/logs/error_log.log",
                    "maxBytes": 10000,
                    "backupCount": 10,
                    "delay": "True",
                },
                "access_file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "formatter": "access",
                    "filename": "./stock_app/logs/access_log.log",
                    "maxBytes": 10000,
                    "backupCount": 10,
                    "delay": "True",
                }
            }
        }
# ["console"] if debug else ["console", "error_file", "email"]
# ["console"] if debug else ["console", "access_file"]
        std_loggers = {
            "loggers": {
                "app.error": {
                    "handlers": ['error_file'],
                    "level": "INFO",
                    "propagate": False,
                },
                "app.access": {
                    "handlers": ["access_file"],
                    "level": "INFO",
                    "propagate": False,
                }
            }
        }

        log_config = {
            "version": 1,
            # "disable_existing_loggers": True,
            "formatters": std_formatters["formatters"],
            "loggers": std_loggers["loggers"],
            "handlers": std_handlers["handlers"],
        }
        dictConfig(log_config)