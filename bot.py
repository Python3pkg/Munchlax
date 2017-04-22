from slack import Slack

class Command(object):
    def __init__(self, cmd, func, requires):
        self.cmd = cmd
        self.requires = requires
        self.func = func

class Bot(object):
    def __init__(self):
        self._slack = None
        self._commands = {}

    ########################################
    # COMMAND REGISTRATION DECORATOR
    ########################################

    def command(self, cmd=None, requires=[]):
        def dec(func):
            if cmd is None:
                cmd = func.__name__

            self._commands[cmd] = Command(cmd, func, requires)
            return func
        return dec

    ########################################
    # EVENT HANDLERS
    ########################################

    def _handle_message(self, message):
        if not self._check_prefix(message.text):
            return

    ########################################
    # EXPOSED FUNCTiONS
    ########################################

    def start(self, token):
        self._slack = Slack()
        self._slack.set_token(token)
        self._slack.on('message', self._handle_message)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._slack.listen())