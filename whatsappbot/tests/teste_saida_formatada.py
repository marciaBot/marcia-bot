from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import os
import re

"""
list_conversa = open(os.getcwd()+"/whatsappbot/Conversa_Formatada.txt", "r")
list_conversa = [c.replace("\n", "") for c in list_conversa]
chatbot = ChatBot('Elielson_bot')
trainer = ListTrainer(chatbot)

trainer.train([
    "Oi",
    "Olá, tudo bem? O que deseja?",
    "Gostaria de comprar Parecetamol",
    "Certo, o senhor já é cadastrado?",
    "Não sou",
    "Pode me informar seu CPF?",
    "017.725.412-22",
    "Qual o bairro que você mora?",
    "Pedreira",
    "Qual a avenida?",
    "Visconde",
    "Qual o número de sua casa?",
    "1557",
    "Certo, seu cadastro foi feito!",
    "Obrigado",
    "De nada",
    "Eu gostaria de comprar um parecetamol",
    "O senhor já é cadastrado?",
    "Sim",
    "Me informe seu CPF",
    "017.725.412-22",
    "Irei verificar se há disponibilidade do parecetamol em nosso estoque, um minuto",
    "Tudo bem, obrigado",
    "Há disponibilidade no estoque, quantos o senhor deseja?",
    "2",
    "O senhor irá pagar no débito ou crédito?",
    "Crédito",
    "Certo, estaremos enviando seu remédio o mais rápido possível, obrigado por comprar conosco!",
    "Obrigado"
])
"""
while False:
    pergunta = input("você: ")
    response = chatbot.get_response(pergunta)
    print("Bot: ", response)

