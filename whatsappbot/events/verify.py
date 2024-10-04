from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from requests import put as put_api
from fuzzywuzzy import process, fuzz
from .register import cadastrar_venda
from ..db import lista_produtos, limpar_lista_produtor, cadastros_novos
from ..extensions.alert_people import AlertPeople
from ..services.validate_users import format_number, GET_NAME

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
        #status = post_api('https://marcia-bot-patient-cloud-6675.fly.dev/item-venda', json=item_venda).status_code
        #print("Status item venda: ", status)
    venda['obs'] = "Forma de pagamento será em: "+forma_pagamento
    #status = put_api('https://marcia-bot-patient-cloud-6675.fly.dev/venda/{}'.format(venda['id']), json=venda).status_code
    #print("Status put Venda: ", status)
    limpar_lista_produtor()
    return "Seu pedido está finalizado e em breve chegará em sua residência!\n\nAh, mais uma coisa, você gostaria que avisássemos o horário que você deve tomar seu remédio?"


@register_call("verificar_cpf")
def verificar_cpf(session, query):
    numero = format_number(query)
    resposta = numero in cadastros_novos
    return "Deseja adicionar esse número em seu cadastro?" if resposta else "Não encontramos seu CPF, deseja cadastrar?"

@register_call("verificar_numero")
def verificar_numero(session, query):
    number = format_number(query)
    #url = 'https://marcia-bot-patient-cloud-6675.fly.dev/cliente/numero/{}'.format(number)
    #resposta = get_api(url)
    marcia_resposta = ""
    numero_cadastrado = number in cadastros_novos
    if numero_cadastrado is False:
        marcia_resposta = "Olá, tudo bem? Vimos que seu número não está cadastrado, você já possui cadastro?"
    else:
        nome = cadastros_novos[number]["nome"]
        nome = nome.capitalize()
        session.memory['nome'] = nome
        marcia_resposta = "Olá, {}, tudo bem? O que você deseja?".format(nome)
    return marcia_resposta

@register_call("verificar_produto")
def verificar_produto(session, query):
    
    medicine, quantidade, numero = query.split(',')
    medicine, quantidade, numero = [medicine.strip(), quantidade.strip(), numero.strip()]
    numero = format_number(numero)
    remedios = lista_produtos
    remedios_nomes = [p['nome'].lower() for p in remedios]
    remedio_encontrado = process.extractOne(medicine, remedios_nomes, scorer=fuzz.token_sort_ratio, score_cutoff=75)
    remedio_encontrado = remedio_encontrado[0] if remedio_encontrado is not None else None
    
    if remedio_encontrado:
        if not verificar_cliente_possui_venda(numero):
            cliente = get_api('https://marcia-bot-patient-cloud-6675.fly.dev/cliente/numero/{}'.format(numero)).json()
            print("Status cadastro venda: ", cadastrar_venda(cliente['clienteId']))
        preco = [p['preco'] for p in remedios if p['nome'].lower() == remedio_encontrado][0]
        id_remedio = [p['id'] for p in remedios if p['nome'].lower() == remedio_encontrado][0]
        preco = preco*int(quantidade)
        lista_produtos.append({'remedio': remedio_encontrado , 'quantidade': quantidade, 'preco_total': preco, 'id': id_remedio})
        return 'Você gostaria de comprar {} {}?'.format(quantidade, remedio_encontrado)
    return "Desculpe, mas não encontramos nenhum remédio com este nome: {}".format(medicine)

def verificar_cliente_possui_venda(numero):
    
    cliente = get_api('https://marcia-bot-patient-cloud-6675.fly.dev/cliente/numero/{}'.format(numero)).json()
    vendas = get_api('https://marcia-bot-patient-cloud-6675.fly.dev/venda')
    vendas_status = vendas.status_code
    vendas = vendas.json()
    venda_cliente = []
    if len(vendas) > 0 and vendas_status == 200:
        venda_cliente = [v for v in vendas if v['clienteId'] == cliente['clienteId']]
    if len(venda_cliente) > 0:
        return True
    return False

def ultima_venda_cliente(numero):
    cliente = get_api('https://marcia-bot-patient-cloud-6675.fly.dev/cliente/numero/{}'.format(numero)).json()
    vendas = get_api('https://marcia-bot-patient-cloud-6675.fly.dev/venda').json()
    venda_cliente = [v for v in vendas if v['clienteId'] == cliente['clienteId']]
    if len(venda_cliente) > 0:
        return venda_cliente[-1]
    return None


