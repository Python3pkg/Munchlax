from .async import async_wrapper

class Message(object):
    def __init__(self, loop, client, message):
        self.__dict__.update(message.__dict__)
        self._loop = loop
        self._client = client

    async def reply(self, text=None, file=None):
        if file is None:
            if text is None:
                return

            await async_wrapper(
                self._loop,
                self._client.api_call,
                'chat.postMessage',
                channel=self.channel.id,
                text=text
            )
        else:
            await async_wrapper(
                self._loop,
                self._client.api_call,
                'files.upload',
                channels=self.channel.id,
                initial_comment=text,
                **file
            )

    async def addReaction(self, name):
        await async_wrapper(
            self._loop,
            self._client.api_call,
            'reactions.add',
            channel=self.channel.id,
            timestamp=self.ts,
            name=name
        )