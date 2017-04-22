from .object import Object
from .async import async_wrapper

class Channel(Object):
    def __init__(loop, client, channel):
        Object.__init__(self, message)
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
            ))