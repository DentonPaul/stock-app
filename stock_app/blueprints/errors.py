'''Application error handlers.'''
from flask import Blueprint, render_template
import logging

errors = Blueprint('errors', __name__)

## catch all - 500 ##
@errors.app_errorhandler(500)
def internal_server(exception): # pragma: no cover
    # this will go to info_file.log
    logging.info('ERROR occured. Look in error_file.log')
    # will go to error_file.log and email (email does not work on heroku)
    # logging.error(exception, exc_info=True) # will go to error_file.log and email (does not work on heroku)
    return render_template('errors/500.html'), 500  

@errors.app_errorhandler(404)
def page_not_found(exception): # pragma: no cover
    # this will go to info_file.log
    logging.info('ERROR occured. Look in error_file.log')
    # will go to error_file.log and email (email does not work on heroku)
    # logging.error(exception, exc_info=True) 
    return render_template('errors/404.html'), 404  