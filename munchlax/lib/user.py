from .object import Object

class User(Object):
    def __init__(self, slack, user):
        Object.__init__(self, user)
        self._slack = slack