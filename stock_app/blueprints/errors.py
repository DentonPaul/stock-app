'''Application error handlers.'''
from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(500)
def handle_error(exception):
    return render_template('errors/500.html'), 500  # pragma: no cover

@errors.app_errorhandler(404)
def handle_error(exception):
    return render_template('errors/404.html'), 404  # pragma: no cover