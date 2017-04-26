from .object import Object

class Message(Object):
    def __init__(self, slack, message):
        Object.__init__(self, message)
        self._slack = slack

    async def reply(self, text, **kwargs):
        return await self._slack.raw_write(text=text, channel=self.channel, **kwargs)

    async def delete(self):
        return await self._slack.delete(self)

    async def edit(self, text, **kwargs):
        msg = await self._slack.edit(text, self, **kwargs)
        self.__dict__.update(msg.__dict__)
        return self

    async def get_author(self):
        if getattr(self, 'user', None) is not None:
            return await self._slack.user_by_id(self.user)
        elif getattr(self, 'bot', None) is not None:
            return await self._slack.bot_by_id(self.bot)
        else:
            return None

    async def get_channel(self):
        return await self._slack.channel_by_id(self.id)

    async def get_replies(self):
        channel = await self.get_channel()
        return await self._slack.get_channel_replies(channel, self.ts)