class BaseError(Exception):
    def __init__(self, message, status_code):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def serialize(self):
        return {'message': self.message, 'status': self.status_code}

class InvalidClientInput(BaseError):
    def __init__(self, message):
        super(InvalidClientInput,self).__init__(message, 400)
