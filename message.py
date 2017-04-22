class Message(object):
    def __init__(json, client):
        self._client = client
        self.__dict__.update(json)