import os

class Config(object):
    SECRET_KEY = os.environ.get('secret') or 'key-the-secret'

