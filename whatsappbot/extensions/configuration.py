from importlib import import_module
from dynaconf import FlaskDynaconf

def load_modules(app):
    for module in app.config.get("EXTENSIONS"):
        mod = import_module(module)
        mod.init_app(app)

def init_app(app):
    FlaskDynaconf(app)