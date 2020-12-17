from flask import Blueprint, render_template, url_for, redirect, request, make_response, current_app
import logging

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home/index.html')

@home.route("/logstatus", methods=["GET"])
def logs_status(): # pragma: no cover
    logging.debug('This will not go anywhere in production. Will go to console in development/debug mode')
    logging.info('This will go to info_file.log as "root" logger')
    logging.warning('This will go to error_file.log and email')
    logging.error('This will go to error_file.log and email')
    logging.critical('This will go to error_file.log and email')
    logging.exception('This will go to error_file.log and email')
    return make_response("LOGS ARE A SUCCESS", 200)

@home.route('/lookup', methods=['POST'])
def lookup():
    return redirect(url_for('stock.quote', ticker=request.form['ticker']))