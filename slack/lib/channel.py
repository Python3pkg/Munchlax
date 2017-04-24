import asyncio
from .object import Object
from .async import async_wrapper

class Channel(object):
    def __init__(self, loop, client, channel):
        self.__dict__.update(channel.__dict__)
        self._loop = loop
        self._client = client

    async def write(self, **kwargs):
        await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.postMessage',
            channel=self.id,
            **kwargs
        )

    async def upload_file(self, **kwargs):
        await async_wrapper(
            self._loop,
            self._client.api_call,
            'files.upload',
            channels=self.id,
            **kwargs
        )