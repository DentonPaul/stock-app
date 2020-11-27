from flask import Flask
from blueprints.stock import stock
from blueprints.home import home

app = Flask(__name__)

app.register_blueprint(stock, url_prefix='/stock')
app.register_blueprint(home)


    
