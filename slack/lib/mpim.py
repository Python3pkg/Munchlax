from .object import Object

class MPIM(Object):
    def __init__(self, slack, MPim):
        Object.__init__(self, MPim)
        self._slack = slack