# from logging.config import dictConfig


class LogSetup(object):
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)

    def init_app(self, app):
        log_type = app.config["LOG_TYPE"]
        logging_level = app.config["LOG_LEVEL"]
        if log_type != "stream":
            try:
                log_directory = app.config["LOG_DIR"]
                app_log_file_name = app.config["APP_LOG_NAME"]
                shift_log_file_name = app.config["SHIFT_LOG_NAME"]
            except KeyError as e:
                exit(code="{} is a required parameter for log_type '{}'".format(e, log_type))
            app_log = "/".join([log_directory, app_log_file_name])
            shift_log = "/".join([log_directory, shift_log_file_name])

        if log_type == "stream":
            logging_policy = "logging.StreamHandler" # just goes to terminal/Output
        elif log_type == "watched":
            logging_policy = "logging.handlers.WatchedFileHandler"
        elif log_type == "rotating":
            log_max_bytes = app.config["LOG_MAX_BYTES"]
            log_copies = app.config["LOG_COPIES"]
            logging_policy = "logging.handlers.RotatingFileHandler"
        elif log_type == "timed_rotating":
            log_copies = app.config["LOG_COPIES"]
            log_when = app.config["LOG_WHEN"]
            log_interval = app.config["LOG_INTERVAL"]
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
                        "level": app.config["MAIN_LOG_LEVEL"], # logging level for main log (app.log)
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
            "disable_existing_loggers": True,
            "formatters": std_format["formatters"],
            "loggers": std_logger["loggers"],
            "handlers": logging_handler["handlers"],
        }
        dictConfig(log_config)


        "handlers_default": {
            "console": { # goes to terminal
                "level": "INFO",
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": "ext://sys.stdout",
            },
            "email": {
                "class": "logging.handlers.SMTPHandler",
                "formatter": "default",
                "level": "ERROR",
                "mailhost": ("smtp.gmail.com", 587),
                "fromaddr": "pythonpracticesms@gmail.com",
                "toaddrs": ["2483285403@vzwpix.com"],
                "subject": "Error Logs",
                "credentials": ("pythonpracticesms@gmail.com", "thisisapassword"),
            },
        }

        if log_type == 'rotating':
            log_max_bytes = app.config["LOG_MAX_BYTES"]
            log_copies = app.config["LOG_COPIES"]
            logging_policy = "logging.handlers.RotatingFileHandler"
            "handlers_additional": {
                "default": {
                        "level": logging_level,
                        "class": logging_policy,
                        "filename": log_dir,
                        "backupCount": log_copies,
                        "maxBytes": log_max_bytes,
                        "formatter": "default",
                        "delay": True,
                    }
                ""
            }

