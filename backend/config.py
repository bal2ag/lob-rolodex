import os

basedir = os.path.abspath(os.path.dirname(__file__))

def boolify(value):
    if not value:
        return False
    if value.lower() == 'false':
        return False
    return True

class Config(object):
    DATE_FORMAT = os.environ["DATE_FORMAT"]
    LOB_API_KEY = os.environ["LOB_API_KEY"]

    @staticmethod
    def init_app(app):
        pass

