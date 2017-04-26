from .object import Object

class Message(Object):
    def __init__(self, slack, message):
        Object.__init__(self, message)
        self._slack = slack

    async def reply(self, **kwargs):
        return await self._slack.write(channel=self.channel, **kwargs)

    async def get_author(self):
        if getattr(self, 'user', None) is not None:
            return await self._slack.user_from_id(self.user)
        elif getattr(self, 'bot', None) is not None:
            return await self._slack.bot_from_id(self.bot)
        else:
            return None