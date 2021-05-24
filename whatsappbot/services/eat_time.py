import threading
from twilio.rest import Client
import time

class EatTime():

    def __init__(self, whats=None, med=None, time=None, name=None):
        self.whatsapp = whats
        self.name = name
        self.medicine = med
        self.time = time
        self.account_sid = "ACcb9ced49169d33bbfbfa709617ec330c"
        self.auth_token  = "2899ce7db8a565aafa5851a7ee956d30"
        self.client = Client(account_sid, auth_token)

    def is_hour_to_eat(self):
        now_time = str(time.localtime().tm_hour)+":"+str(time.localtime().tm_min)
        if now_time == self.time:
            return True
        return False
    
    def send_message(self):
        if self.is_hour_to_eat():
            msg_good_day = self.msg_day()
            message = client.messages.create(
                from_="whatsapp:+14155238886",
                body="Olá, {}, está na hora de você tomar {}. Espero que esteja tudo bem, tenha um {} :)".format(self.name, self.medicine, msg_good_day),
                to=self.whatsapp, 
            )

    def msg_day(self):
        hour_day = time.localtime().tm_hour
        if 12 > hour_day >= 6:
            return "bom dia"
        elif 18 > hour_day >= 12:
            return "boa tarde"
        else:
            return "boa noite"

    