from .object import Object

class Group(Object):
    def __init__(self, slack, group):
        Object.__init__(self, group)
        self._slack = slack