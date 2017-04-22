import asyncio
from .object import Object
from .async import async_wrapper

class Channel(object):
    def __init__(self, loop, client, channel):
        self.__dict__.update(channel.__dict__)
        self._loop = loop
        self._client = client

    async def write(self, text=None, file=None):
        if file is None:
            if text is None:
                return

            await async_wrapper(
                self._loop,
                self._client.api_call,
                'chat.postMessage',
                channel=self.id,
                text=text
            )
        else:
            await async_wrapper(
                self._loop,
                self._client.api_call,
                'files.upload',
                channels=self.id,
                initial_comment=text,
                **file
            )