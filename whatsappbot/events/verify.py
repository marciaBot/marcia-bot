from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import *
import ast

@register_call("verificar_cpf")
def verificar_cpf(session, query):
    resposta = get_api('https://marcia-api.herokuapp.com/cliente/cpf/{}'.format(query)).status_code
    return "Deseja adicionar esse número em seu cadastro?" if query in fake_cpfs else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    number = query.strip().replace('\\', "")
    url = 'https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)
    resposta = get_api(url)
    marcia_resposta = ""
    if resposta.status_code == 404:
        marcia_resposta = "Olá, tudo bem? Vimos que seu número não está cadastrado, você já possui cadastro?"
    else:
        nome = GET_NAME.search(resposta.json()['nome']).group()
        nome = nome.capitalize()
        marcia_resposta = "Olá, {}, tudo bem? O que você deseja?".format(nome)
    return  marcia_resposta