from flask import Blueprint, render_template, url_for, redirect, request, make_response, current_app
import logging

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home/index.html')

@home.route("/logstatus", methods=["GET"])
def logs_status(): # pragma: no cover
    logging.getLogger('app.info').info('this goes to info_file.log')
    logging.getLogger('app.error').error('this goes to error_file.log')
    logging.getLogger('root').info('this goes to terminal')
    logging.getLogger('app.email').info('this should be emailed to dp.midfielder7@gmail.com')
    return make_response("LOGS ARE A SUCCESS", 200)

@home.route('/lookup', methods=['POST'])
def lookup():
    return redirect(url_for('stock.quote', ticker=request.form['ticker']))