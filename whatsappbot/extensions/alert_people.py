import threading
from time import sleep

class AlertPeople():


    def __init__(self):
        self.peoples_to_alert = []
        thread = threading.Thread(target=self.keep_processing, args=())
        thread.daemon = True
        thread.start()

    def init_app(self, app):
        app.alert_people = self

    def keep_processing(self):
        while True:
            self.process()
            sleep(1)

    def process(self):
        if not self.peoples_to_alert:
            return
        for people in self.peoples_to_alert:
            if people.is_hour_to_eat():
                people.send_message()

    def add_people(self, people):
        self.peoples_to_alert.append(people)

def init_app(app):
    app.alert_people = AlertPeople()