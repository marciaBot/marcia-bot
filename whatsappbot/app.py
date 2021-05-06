from flask import Flask
from .extensions.configuration import load_modules
from .extensions.configuration import init_app as init_conf

def create_app():
    app = Flask(__name__)
    init_conf(app)
    load_modules(app)
    app.register_blueprint
    return app