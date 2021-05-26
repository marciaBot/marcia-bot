from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from requests import put as put_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import lista_produtos, cadastros_novos, enderecos_novos, limpar_lista_produtor
import ast
from flask import current_app
from whatsappbot.services.eat_time import EatTime
from whatsappbot.extensions.alert_people import AlertPeople
from fuzzywuzzy import process, fuzz
from .register import cadastrar_venda

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

@register_call("verificar_resposta_forma_pagamento")
def verificar_resposta_forma_pagamento(session, query):
    
    numero, forma_pagamento = query.split(",")
    numero, forma_pagamento = [numero.strip(), forma_pagamento.strip()]
    numero = format_number(numero)
    venda = ultima_venda_cliente(numero)
    print(lista_produtos)
    for p in lista_produtos:
        item_venda = {'produtoId': p['id'], 'quantidade': p['quantidade'], 'vendaId': venda['id']}
        status = post_api('https://marcia-api.herokuapp.com/item-venda', json=item_venda).status_code
        print("Status item venda: ", status)
    venda['obs'] = "Forma de pagamento será em: "+forma_pagamento
    status = put_api('https://marcia-api.herokuapp.com/venda/{}'.format(venda['id']), json=venda).status_code
    print("Status put Venda: ", status)
    limpar_lista_produtor()
    return "Seu pedido está finalizado e em breve chegará em sua residência!\n\nAh, mais uma coisa, você gostaria que avisássemos o horário que você deve tomar seu remédio?"


@register_call("verificar_cpf")
def verificar_cpf(session, query):
    resposta = get_api('https://marcia-api.herokuapp.com/cliente/cpf/{}'.format(query)).status_code
    return "Deseja adicionar esse número em seu cadastro?" if query in fake_cpfs else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    number = format_number(query)
    url = 'https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)
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
    
    medicine, quantidade, numero = query.split(',')
    medicine, quantidade, numero = [medicine.strip(), quantidade.strip(), numero.strip()]
    numero = format_number(numero)
    remedios = get_api('https://marcia-api.herokuapp.com/produto').json()
    remedios_nomes = [p['nome'].lower() for p in remedios]
    remedio_encontrado = process.extractOne(medicine, remedios_nomes, scorer=fuzz.token_sort_ratio, score_cutoff=75)
    remedio_encontrado = remedio_encontrado[0] if remedio_encontrado is not None else None
    
    if remedio_encontrado:
        if not verificar_cliente_possui_venda(numero):
            cliente = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(numero)).json()
            print("Status cadastro venda: ", cadastrar_venda(cliente['clienteId']))
        preco = [p['preco'] for p in remedios if p['nome'].lower() == remedio_encontrado][0]
        id_remedio = [p['id'] for p in remedios if p['nome'].lower() == remedio_encontrado][0]
        preco = preco*int(quantidade)
        lista_produtos.append({'remedio': remedio_encontrado , 'quantidade': quantidade, 'preco_total': preco, 'id': id_remedio})
        return 'Você gostaria de comprar {} {}?'.format(quantidade, remedio_encontrado)
    return "Desculpe, mas não encontramos nenhum remédio com este nome: {}".format(medicine)

def verificar_cliente_possui_venda(numero):
    
    cliente = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(numero)).json()
    vendas = get_api('https://marcia-api.herokuapp.com/venda')
    vendas_status = vendas.status_code
    vendas = vendas.json()
    venda_cliente = []
    if len(vendas) > 0 and vendas_status == 200:
        venda_cliente = [v for v in vendas if v['clienteId'] == cliente['clienteId']]
    if len(venda_cliente) > 0:
        return True
    return False

def ultima_venda_cliente(numero):
    cliente = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(numero)).json()
    vendas = get_api('https://marcia-api.herokuapp.com/venda').json()
    venda_cliente = [v for v in vendas if v['clienteId'] == cliente['clienteId']]
    if len(venda_cliente) > 0:
        return venda_cliente[-1]
    return None


