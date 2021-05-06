from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import Chat

marcia = Chat("whatsappbot/templates/conversation.j2")
bp = Blueprint("conversation", __name__)

@bp.route("/")
def home():
    return "funfou"


@bp.route("/bot")
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message(marcia.say(incoming_msg))
    return str(resp)
    return "funfou"

def init_app(app):
    app.register_blueprint(bp)
