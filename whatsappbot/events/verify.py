from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import *
import ast
from flask import current_app
from whatsappbot.services.eat_time import EatTime
from whatsappbot.extensions.alert_people import AlertPeople
from fuzzywuzzy import process, fuzz
alert_people = AlertPeople()

@register_call("verificar_resposta_pedir_mais_alguma_coisa")
def verificar_resposta_pedir_mais_alguma_coisa(session, query):
    if process.extractOne(query, ['sim','isso','s','si','y','ye','yes','yep','yeah', 'quero'], scorer=fuzz.token_sort_ratio, score_cutoff=75):
        return "O que você deseja?"
    remedios_pedidos = [p['remedio'] for p in lista_produtos]
    precos = [p['preco_total'] for p in lista_produtos]
    preco_total = sum(precos)
    resposta = '🛒 Seu pedido foi finalizado e possui os seguintes produtos: \n💊 ' + \
     ', '.join(remedios_pedidos) + \
     '\n🪙 Totalizando em R$ '+ str(round(preco_total, 2)) +"\n" \
     'Seu pagamento será feito em dinheiro, crédito ou débito?'
    return resposta

@register_call("verificar_cpf")
def verificar_cpf(session, query):
    resposta = get_api('https://marcia-api.herokuapp.com/cliente/cpf/{}'.format(query)).status_code
    return "Deseja adicionar esse número em seu cadastro?" if query in fake_cpfs else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    number = format_number(query)
    url = 'https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)
    print(url)
    resposta = get_api(url)
    marcia_resposta = ""
     
    if resposta.status_code == 404:
        marcia_resposta = "Olá, tudo bem? Vimos que seu número não está cadastrado, você já possui cadastro?"
    else:
        nome = GET_NAME.search(resposta.json()['nome']).group()
        nome = nome.capitalize()
        session.memory['nome']=nome
        marcia_resposta = "Olá, {}, tudo bem? O que você deseja?".format(nome)
    return  marcia_resposta

@register_call("verificar_produto")
def verificar_produto(session, query):
    medicine, quantidade = query.split(',')
    medicine, quantidade = [medicine.strip(), quantidade.strip()]
    remedios = get_api('https://marcia-api.herokuapp.com/produto').json()
    remedios_nomes = [p['nome'].lower() for p in remedios]
    remedio_encontrado = process.extractOne(medicine, remedios_nomes, scorer=fuzz.token_sort_ratio, score_cutoff=75)
    
    remedio_encontrado = remedio_encontrado[0] if remedio_encontrado is not None else None
    if remedio_encontrado:
        preco = [p['preco'] for p in remedios if p['nome'].lower() == remedio_encontrado][0]
        preco = preco*int(quantidade)
        lista_produtos.append({'remedio': remedio_encontrado , 'quantidade': quantidade, 'preco_total': preco})
        return 'Você gostaria de comprar {} {}?'.format(quantidade, remedio_encontrado)
    return "Desculpe, mas não encontramos nenhum remédio com este nome: {}".format(medicine)


