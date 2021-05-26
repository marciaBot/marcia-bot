from chatbot import register_call
from requests import get as get_api
from requests import post as post_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import *
import ast
from whatsappbot.services.eat_time import EatTime
from whatsappbot.extensions.alert_people import AlertPeople

alert_people = AlertPeople()

@register_call("alert_client")
def alert_client(session, query):
    formatados = format_number(query)
    number = GET_NUMBER.search(formatados).group().strip()
    hour = GET_HOUR.search(formatados).group().strip()
    medicine = GET_NAME_MEDICINE.search(formatados).group().strip()
    url = 'https://marcia-api.herokuapp.com/cliente/numero/{}'.format(number)
    resposta = get_api(url)
    nome = GET_NAME.search(resposta.json()['nome']).group()
    nome = nome.capitalize()
    new_client_alert = EatTime(number, medicine, hour, nome, 1)
    alert_people.add_people(new_client_alert)
    return "O senhor será avisado sempre nesse horário de 8 em 8 horas :D"