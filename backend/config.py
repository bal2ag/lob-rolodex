import os

basedir = os.path.abspath(os.path.dirname(__file__))

def boolify(value):
    if not value:
        return False
    if value.lower() == 'false':
        return False
    return True

class Config(object):
    LOB_API_KEY = os.environ["LOB_API_KEY"]

    CHRISTMAS_CARD_FILE = os.environ["CHRISTMAS_CARD_TEMPLATE"]
    with open(CHRISTMAS_CARD_FILE, 'r') as f:
        CHRISTMAS_CARD_TEMPLATE = f.read().replace('\n', '')

    @staticmethod
    def init_app(app):
        pass

