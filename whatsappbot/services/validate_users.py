import re
GET_NUMBER = re.compile(r'(\w+\\\:\+\d{12,13})')
GET_VALUES = re.compile(r'.*(?<=\,)')
GET_NAME = re.compile(r'\w+')