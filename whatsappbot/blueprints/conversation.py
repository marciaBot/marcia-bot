from flask import Blueprint, request
from requests import get as get_api
from requests import post as post_api
from twilio.twiml.messaging_response import MessagingResponse
from chatbot import Chat, register_call
import ast
import re

marcia = Chat(default_template="whatsappbot/templates/conversation.j2", language='pt-br')
bp = Blueprint("conversation", __name__)
GET_NUMBER = re.compile(r'(\+\d{12,13})')
GET_VALUES = re.compile(r'.*(?<=\,)')
GET_NAME = re.compile(r'\w+')
fake_cpfs = []
fake_numeros = []
cadastros_novos = {}
enderecos_novos = {}
@bp.route("/")
def home():
    return "funfou"

@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    cadastros_novos[query.strip()] = {}
    enderecos_novos[query.strip()] = {}
    return ""

@register_call("cadastrar_cpf")
def cadastrar_cpf(session, query):
    
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["cpf"] = values
    cadastros_novos[number]["numero"] = number
    return "Me informe sua data de nascimento"


@register_call("cadastrar_data_nascimento")
def cadastrar_data_nascimento(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["dataNascimento"] = values
    return "Qual o seu nome completo?"

@register_call("cadastrar_nome")
def cadastrar_nome(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["nome"] = values
    post_api('https://marcia-api.herokuapp.com/cliente', json=cadastros_novos[number])
    return "Qual o seu bairro?"

@register_call("cadastrar_bairro")
def cadastrar_bairro(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]['bairro'] = values
    return "Qual a sua rua?"

@register_call("cadastrar_rua")
def cadastrar_rua(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["rua"] = values
    return "Qual o número da sua casa?"

@register_call("cadastrar_numero_casa")
def cadastrar_numero_casa(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["numero"] = values
    return "Qual o seu CEP?"

@register_call("cadastrar_cep")
def cadastrar_cep(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["cep"] = values
    return "Qual o complemento para seu endereço?"

@register_call("cadastrar_complemento")
def cadastrar_complemento(session, query):
    number = GET_NUMBER.search(query).group()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["complemento"] = values
    return "Alguma referência para sua localização?"

@register_call("cadastrar_referencia")
def cadastrar_referencia(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["referencia"] = values
    return "Alguma observação?"

@register_call("cadastrar_observacao")
def cadastrar_observacao(session, query):
    number = GET_NUMBER.search(query).group().strip()
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["observacao"] = values
    id_client = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)).json()['clienteId']
    print(id_client)
    enderecos_novos[number]["clienteId"] = int(id_client)
    post_api('https://marcia-api.herokuapp.com/cliente', json=enderecos_novos[number])
    return "Seu cadastrado foi realizado com sucesso! Agora voltando ao seu pedido, o que o senhor deseja?"

@register_call("verificar_cpf")
def verificar_cpf(session, query):
    
    resposta = get_api('https://marcia-api.herokuapp.com/cliente/cpf/{}'.format(query)).status_code
    return "Deseja adicionar esse número em seu cadastro?" if query in fake_cpfs else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    resposta = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(query.strip()))
    marcia_resposta = ""
    if resposta.status_code == 404:
        marcia_resposta = "Olá, tudo bem? Vimos que seu número não está cadastrado, você já possui cadastro?"
    else:
        nome = GET_NAME.search(resposta.json()['nome']).group()
        nome = nome.capitalize()
        marcia_resposta = "Olá, {}, tudo bem? O que você deseja?".format(nome)
    return  marcia_resposta

@bp.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    print(incoming_msg)
    
    numero = request.values.get('From', '').lower().replace("whatsapp:", "").strip()
    resp = MessagingResponse()
    msg = resp.message()
    print(numero+" "+incoming_msg)
    marcia_disse = marcia.say(numero+" "+incoming_msg)
    print(marcia_disse)
    msg.body(marcia_disse)
    return str(resp)
    

def init_app(app):
    app.register_blueprint(bp)
