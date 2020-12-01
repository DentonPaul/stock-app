from logging.config import dictConfig


class LogSetup(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app):
        log_type = "timed_rotating"
        logging_level = "INFO"
        log_directory = "./stock_app/logs/"
        app_log = log_directory + "app_log.log"
        shift_log = log_directory + "shift_log.log"

        # if log_type != "stream":
        #     try:
        #         log_directory = app.config["LOG_DIR"]
        #         app_log_file_name = app.config["APP_LOG_NAME"]
        #         shift_log_file_name = app.config["SHIFT_LOG_NAME"]
        #     except KeyError as e:
        #         exit(code="{} is a required parameter for log_type '{}'".format(e, log_type))
        #     app_log = "/".join([log_directory, app_log_file_name])
        #     shift_log = "/".join([log_directory, shift_log_file_name])

        if log_type == "stream":
            logging_policy = "logging.StreamHandler" # just goes to terminal/Output
        elif log_type == "rotating":
            log_max_bytes = app.config["LOG_MAX_BYTES"]
            log_copies = app.config["LOG_COPIES"]
            logging_policy = "logging.handlers.RotatingFileHandler"
        elif log_type == "timed_rotating":
            log_copies = 2
            log_when = "midnight"
            log_interval = 1
            logging_policy = "logging.handlers.TimedRotatingFileHandler"            
        else:
            raise Exception(logtype + " is not a valid log type.")
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
        if log_type == "stream":
            logging_handler = {
                "handlers": {
                    "default": {
                        "level": logging_level,
                        "formatter": "default",
                        "class": logging_policy,
                    },
                    "shift_logs": {
                        "level": logging_level,
                        "class": logging_policy,
                        "formatter": "shift",
                    },
                }
            }
        elif log_type == "watched":
            logging_handler = {
                "handlers": {
                    "default": {
                        "level": logging_level,
                        "class": logging_policy,
                        "filename": app_log,
                        "formatter": "default",
                        "delay": True,
                    },
                    "shift_logs": {
                        "level": logging_level,
                        "class": logging_policy,
                        "filename": shift_log,
                        "formatter": "shift",
                        "delay": True,
                    },
                }
            }
        elif log_type == "rotating":
            logging_handler = {
                "handlers": {
                    "default": {
                        "level": logging_level,
                        "class": logging_policy,
                        "filename": app_log,
                        "backupCount": log_copies,
                        "maxBytes": log_max_bytes,
                        "formatter": "default",
                        "delay": True,
                    },
                    "shift_logs": {
                        "level": logging_level,
                        "class": logging_policy,
                        "filename": shift_log,
                        "backupCount": log_copies,
                        "maxBytes": log_max_bytes,
                        "formatter": "shift",
                        "delay": True,
                    },
                }
            }
        else:
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