from .object import Object

class Channel(Object):
    def __init__(self, slack, channel):
        Object.__init__(self, channel)
        self._slack = slack