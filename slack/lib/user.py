from .async import async_wrapper

class User(object):
    def __init__(self, loop, client, user):
        self.__dict__.update(user.__dict__)
        self._loop = loop
        self._client = client