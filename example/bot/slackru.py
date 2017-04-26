from slack.bot import Bot

class SlackRU(Bot):
    def __init__(self):
        Bot.__init__(self)
        self.mentor_channel = None