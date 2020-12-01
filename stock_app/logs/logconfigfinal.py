from logging.config import dictConfig

class LogSetup(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app):
        logging_policy = "logging.handlers.TimedRotatingFileHandler" 
        logging_level = "INFO"
        log_directory = "./stock_app/logs/"
        app_log = log_directory + "app_log.log"
        shift_log = log_directory + "shift_log.log"
        log_copies = 2
        log_when = "midnight"
        log_interval = 1

        std_format = {
            "formatters": {
                "default": {
                    "format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s: %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "shift": {"format": "[%(asctime)s.%(msecs)03d] %(levelname)s %(name)s:%(funcName)s: %(message)s", 
                          "datefmt": "%Y-%m-%d %H:%M:%S"}
            }
        }

        std_logger = {
            "loggers": {
                "": {"level": logging_level, "handlers": ["default"], "propagate": True},
                "app.shift": {
                    "level": logging_level,
                    "handlers": ["shift_logs"],
                    "propagate": False,
                },
                "root": {"level": logging_level, "handlers": ["default"]},
            }
        }

        logging_handler = {
            "handlers": {
                "default": {
                    "level": "INFO", # logging level for main log (app.log)
                    "class": logging_policy,
                    "filename": app_log,
                    "backupCount": log_copies,
                    "when": log_when,
                    "interval": log_interval,
                    "formatter": "default",
                    # add custom suffix for files
                    "delay": True,
                },
                "shift_logs": {
                    "level": logging_level,
                    "class": logging_policy,
                    "filename": shift_log,
                    "backupCount": log_copies,
                    "when": log_when,
                    "interval": log_interval,
                    "formatter": "shift",
                    # add custom suffix for files
                    "delay": True,
                },
            }
        }

        log_config = {
            "version": 1,
            "disable_existing_loggers": True, # maybe remove this
            "formatters": std_format["formatters"],
            "loggers": std_logger["loggers"],
            "handlers": logging_handler["handlers"],
        }
        dictConfig(log_config)