'''Application error handlers.'''
from flask import Blueprint, render_template
import logging

errors = Blueprint('errors', __name__)

## catch all - 500 ##
@errors.app_errorhandler(500)
def handle_error(exception): # pragma: no cover
    logging.getLogger('app.access').error('There was an error: ' + str(exception))
    logging.getLogger('app.error').error(exception, exc_info=True)
    # logging.getLogger('app.email').error('hello there')  ## DOES NOT WORK ON HEROKU
    return render_template('errors/500.html'), 500  # pragma: no cover

@errors.app_errorhandler(404)
def handle_error(exception): # pragma: no cover
    logging.getLogger('app.error').error(exception, exc_info=True)
    return render_template('errors/404.html'), 404  # pragma: no cover