from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from whatsappbot.events import marcia


bp = Blueprint("conversation", __name__)

@bp.route("/")
def home():
    return "funfou"


@bp.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body').lower()
    numero = request.values.get('From').strip()
    resp = MessagingResponse()
    msg = resp.message()
    marcia_disse = marcia.say(numero+" "+incoming_msg)
    msg.body(marcia_disse)
    return str(resp)

    
def init_app(app):
    app.register_blueprint(bp)
