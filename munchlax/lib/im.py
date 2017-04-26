from .object import Object

class IM(Object):
    def __init__(self, slack, im):
        Object.__init__(self, im)
        self._slack = slack