from flask import Flask, render_template
from stock_app.blueprints.stock import stock
from stock_app.blueprints.home import home
from stock_app.blueprints.errors import errors
from stock_app.config import connfigurations
from stock_app.logs.logconfig import LogSetup

def create_app(env_name="dev"):
    app = Flask(__name__)
    app.config.from_object(connfigurations[env_name])

    initialize_logging(app)
    register_all_blueprints(app, env_name)
 
    return app

def register_all_blueprints(app, env_name):
    if env_name.lower() == 'prod':
        app.register_blueprint(errors) # pragma: no cover
    app.register_blueprint(stock, url_prefix='/stock')
    app.register_blueprint(home)

def initialize_logging(app):
    logs = LogSetup()
    logs.init_app(app)

app = create_app('prod') # (for heroku to launch app)