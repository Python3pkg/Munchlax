from .object import Object
from .async import async_wrapper
from .channel import Channel

class Message(Object):
    def __init__(loop, client, message):
        Object.__init__(self, message)
        self._loop = loop
        self._client = client

        self.channel = Channel(self.channel)

    async def reply(self, text=None, file=None):
        if file is None:
            if text is None:
                return

            await async_wrapper(
                self._loop,
                self._client.api_call,
                'chat.postMessage',
                channel=self.channel,
                text=text,
                thread_ts=self.ts,
            )
        else:
            await async_wrapper(
                self._loop,
                self._client.api_call,
                'files.upload',
                channels=self.channel,
                initial_comment=text,
                **file
            )

    async def addReaction(self, name):
        await async_wrapper(
            self._loop
            self._client.api_call,
            'reactions.add',
            channel=self.channel,
            timestamp=self.ts,
            name=name
        )