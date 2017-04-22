class Object(object):
    def __init__(d):
        def bind(x):
            if isinstance(x, dict):
                return Object(x)
            else:
                return x

        for k, v in d:
            if isinstance(v, list):
                self.__dict__[k] = [bind(x) for x in v]
            else:
                self.__dict__[k] = bind(v)