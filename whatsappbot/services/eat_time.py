import threading
from twilio.rest import Client
import time

class EatTime():

    def __init__(self, whats=None, med=None, time=None, name=None, time_add=0):
        self.whatsapp = whats
        self.name = name
        self.medicine = med
        self.time = time
        self.time_add = time_add
        self.account_sid = "ACbaa882bceb49d813a37ac1b572e12a15"
        self.auth_token  = "15d0965d5b2c1e52adab012a31d21c73"
        self.client = Client(self.account_sid, self.auth_token)

    def is_hour_to_eat(self):
        hour = str(time.localtime().tm_hour)
        minute = str(time.localtime().tm_min)
        minute = minute if len(minute) == 2 else "0"+minute
        now_time = hour+":"+minute
        if now_time == self.time:
            return True
        return False
    
    def send_message(self):
        if self.is_hour_to_eat():
            print("ANTES: ",self.time)
            msg_good_day = self.msg_day()
            message = self.client.messages.create(
                from_="whatsapp:+14155238886",
                body="⏰ Olá, {}, está na hora de você tomar {}. Espero que esteja tudo bem, tenha {} :)".format(self.name, self.medicine, msg_good_day),
                to=self.whatsapp, 
            )
            self.change_time_to_eat()
            print("DEPOIS: ",self.time)


    def msg_day(self):
        hour_day = time.localtime().tm_hour
        if 12 > hour_day >= 6:
            return "um bom dia"
        elif 18 > hour_day >= 12:
            return "uma boa tarde"
        else:
            return "uma boa noite"

    def change_time_to_eat(self):
        now_hour = time.localtime().tm_hour
        new_hour = now_hour+self.time_add
        minute = self.time.split(":")[1]
        self.time = "{}:{}".format(new_hour, minute)