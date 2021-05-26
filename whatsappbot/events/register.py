from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import *
import ast

@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    number = format_number(query)
    cadastros_novos[number] = {}
    enderecos_novos[number] = {}
    return ""

@register_call("cadastrar_cpf")
def cadastrar_cpf(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["cpf"] = values
    cadastros_novos[number]["numero"] = number
    return "Me informe sua data de nascimento"

@register_call("cadastrar_data_nascimento")
def cadastrar_data_nascimento(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["dataNascimento"] = values
    return "Qual o seu nome completo?"

@register_call("cadastrar_nome")
def cadastrar_nome(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    cadastros_novos[number]["nome"] = values
    post_api('https://marcia-api.herokuapp.com/cliente', json=cadastros_novos[number])
    return "Qual o seu bairro?"

@register_call("cadastrar_bairro")
def cadastrar_bairro(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]['bairro'] = values
    return "Qual a sua rua?"

@register_call("cadastrar_rua")
def cadastrar_rua(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["rua"] = values
    return "Qual o número da sua casa?"

@register_call("cadastrar_numero_casa")
def cadastrar_numero_casa(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["numero"] = values
    return "Qual o seu CEP?"

@register_call("cadastrar_cep")
def cadastrar_cep(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["cep"] = values
    return "Qual o complemento para seu endereço?"

@register_call("cadastrar_complemento")
def cadastrar_complemento(session, query):
    number = GET_NUMBER.search(query).group()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["complemento"] = values
    return "Alguma referência para sua localização?"

@register_call("cadastrar_referencia")
def cadastrar_referencia(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["referencia"] = values
    return "Alguma observação?"

@register_call("cadastrar_observacao")
def cadastrar_observacao(session, query):
    number = GET_NUMBER.search(query).group().strip()
    number = format_number(number)
    values = GET_VALUES.search(query).group().replace("(", "").replace(",", "").strip()
    enderecos_novos[number]["observacao"] = values
    id_client = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)).json()['clienteId']
    enderecos_novos[number]["clienteId"] = int(id_client)
    print(enderecos_novos)
    print(enderecos_novos[number])
    resposta = post_api('https://marcia-api.herokuapp.com/endereco', json=enderecos_novos[number])
    print(resposta.status_code)
    return "Seu cadastrado foi realizado com sucesso! Agora voltando ao seu pedido, o que o senhor deseja?"

def cadastrar_venda(id_cliente):
    nova_venda = {'aprovado': False, 'clienteId': id_cliente, 'obs': ''}
    return post_api('https://marcia-api.herokuapp.com/venda', json=nova_venda).status_code


