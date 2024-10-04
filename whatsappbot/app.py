from flask import Flask
from whatsappbot.extensions.configuration import load_modules
from whatsappbot.extensions.configuration import init_app as init_conf


def create_app():
    app = Flask(__name__)
    init_conf(app)
    load_modules(app)
    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
