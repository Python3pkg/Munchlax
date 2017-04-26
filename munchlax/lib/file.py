from .object import Object

class File(Object):
    def __init__(self, slack, file):
        Object.__init__(self, file)
        self._slack = slack