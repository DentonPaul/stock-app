from flask import Flask, render_template
from stock_app.blueprints.stock import stock
from stock_app.blueprints.home import home
from stock_app.config import connfigurations

def create_app(environment_name="dev"):
    app = Flask(__name__)
    app.config.from_object(connfigurations[environment_name])

    @app.errorhandler(500)
    def handle_error(exception):
        return render_template('500.html'), 500  # pragma: no cover (for pytest to ignore line)

    app.register_blueprint(stock, url_prefix='/stock')
    app.register_blueprint(home)
    return app

app = create_app('prod') # this line is for heroku, do not need in vscode


    
