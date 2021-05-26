import re
GET_NUMBER = re.compile(r'(\w+?:\+\d{12,13})')
GET_VALUES = re.compile(r'.*(?<=\,)')
GET_NAME = re.compile(r'\w+')
GET_NAME_MEDICINE = re.compile(r'(\s\D\w+\w)')
GET_HOUR = re.compile(r'\d{2}\:\d{2}')
def format_number(number):
    number = number.strip().replace('\\', '')
    return number