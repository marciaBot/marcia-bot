from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import Chat, register_call

marcia = Chat(default_template="whatsappbot/templates/conversation.j2", language='pt-br')
bp = Blueprint("conversation", __name__)
fake_cpfs = []
fake_numeros = []
@bp.route("/")
def home():
    return "funfou"

@register_call("cadastrar_cpf")
def cadastrar_cpf(session, query):
    print("CPF CADASTRAD: ", query)
    fake_cpfs.append(query)
    return "Obrigada! Seu CPF foi cadastrado :)"

@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    print("NÚMERO CADASTRAD: ", query)
    fake_numeros.append(query)
    return ""

@register_call("verificar_cpf")
def verificar_cpf(session, query):
    print(session)
    return "Deseja adicionar esse número em seu cadastro?" if query in fake_cpfs else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    print(query)
    return "Olá, tudo bem? Vimos que seu número não está cadastrado, você já possui cadastro?" if query not in fake_numeros else "Olá, tudo bem? O que você deseja?"

@bp.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    numero = request.values.get('From', '').lower().replace("whatsapp:", "").strip()
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(marcia.say(numero+" "+incoming_msg))
    return str(resp)
    

def init_app(app):
    app.register_blueprint(bp)
