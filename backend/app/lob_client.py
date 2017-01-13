from flask import current_app

class LobClient(object):
    """Allows deferment of lob API initialization until an application object
    is in context (to make it easier to switch between environments)."""
    def __init__(self):
        import lob
        lob.api_key = current_app.config["LOB_API_KEY"]
        self.lob = lob
