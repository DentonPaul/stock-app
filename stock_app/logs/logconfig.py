import logging
from logging.config import dictConfig
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

# sets up logging for flask app
class LogSetup(object): # pragma: no cover
    def __init__(self, app=None, **kwargs):
        if app is not None:
            self.init_app(app, **kwargs)
    
    def init_app(self, app):
        debug = app.debug

        logging_config = dict(
            version=1,
            disable_existing_loggers=True,
            formatters={
                "default": {
                    "format": "[%(asctime)19s] [%(levelname)8s] : %(message)s (%(filename)s: %(lineno)s)",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
                "info": {
                    "format": "[%(asctime)19s] [%(levelname)8s] : %(message)s (%(filename)s: %(lineno)s)",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                }
            },
            handlers={
                "console": {
                    "level": "INFO",
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                }, 
                "email": {
                    "level": "INFO",
                    "class": "stock_app.logs.logconfig.TlsSMTPHandler",
                    "formatter": "default",
                    "mailhost": app.config['LOG_EMAIL_MAILHOST'],
                    "fromaddr": app.config['LOG_EMAIL_FROMADDR'],
                    "toaddrs": app.config['LOG_EMAIL_TOADDRS'],
                    "subject": app.config['LOG_EMAIL_SUBJECT'],
                    "credentials": (app.config['LOG_EMAIL_FROMADDR'], app.config['LOG_EMAIL_PWD']),
                },
                "error_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "default",
                    "filename": app.config['LOG_FILE_PATH'] + app.config['LOG_ERROR_NAME'],
                    "when": app.config['LOG_WHEN'],
                    "interval": app.config['LOG_INTERVAL'],
                    "backupCount": app.config['LOG_BACKUP_COUNT'],
                    "delay": "True",
                },
                "info_file": {
                    "class": "logging.handlers.TimedRotatingFileHandler",
                    "formatter": "info",
                    "filename": app.config['LOG_FILE_PATH'] + app.config['LOG_INFO_NAME'],
                    "when": app.config['LOG_WHEN'],
                    "interval": app.config['LOG_INTERVAL'],
                    "backupCount": app.config['LOG_BACKUP_COUNT'],
                    "delay": "True",
                }
            },
            # if you want to test functionality of loggers in testing 
            # then get rid of ["console"] if debug else
            loggers={ 
                "app.error": {
                    "level": "INFO",
                    "handlers": ["console"] if debug else ["error_file"],
                    "propagate": False,
                },
                "app.info": {
                    "level": "INFO",
                    "handlers": ["console"] if debug else ["info_file"],
                    "propagate": False,
                },
                "app.email": {
                    "level": "INFO",
                    "handlers": ['console'] if debug else ["email"],
                    "propagate": False,
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["console"],
                    "propagate": True,
                }
            }
        )

        dictConfig(logging_config)

## Gmail support
class TlsSMTPHandler(logging.handlers.SMTPHandler): # pragma: no cover
    def emit(self, record):
        """
        Emit a record.
 
        Format the record and send it to the specified addressees.
        """
        msg = MIMEMultipart()

        msg['Subject'] = self.getSubject(record)
        msg['From'] = self.fromaddr

        text =  MIMEText(self.format(record))
        msg.attach(text)

        email = self.fromaddr
        pas = self.password
        smtp = self.mailhost
        port = self.mailport

        server = smtplib.SMTP(smtp, port)
        # Starting the server
        server.ehlo()
        server.starttls()
        server.ehlo()
        # Now we need to login
        server.login(email, pas)

        for toaddrs in self.toaddrs:
            msg['To'] = toaddrs
            server.sendmail(email, toaddrs, msg.as_string())

        # quit the server
        server.quit()