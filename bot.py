class Command(object):
    def __init__(self, cmd, func, requires):
        self.cmd = cmd
        self.requires = requires
        self.func = func

_commands = {}

class Bot(object):
    def command(cmd=None, requires=[]):
        def dec(func):
            if cmd is None:
                cmd = func.__name__

            _commands[cmd] = Command(cmd, func, requires)
            return func
        return dec