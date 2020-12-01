from flask import Blueprint, render_template, url_for, redirect, request, make_response
import logging

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template('home/index.html')

@home.route("/status", methods=["GET"])
def health_check(): # pragma: no cover
    logging.debug("debug log")
    logging.info("info log")
    logging.warning("warning log")
    logging.error("error log")
    # logging.exception("exception log")
    
    return make_response("OK", 200)

@home.route('/lookup', methods=['POST'])
def lookup():
    return redirect(url_for('stock.quote', ticker=request.form['ticker']))