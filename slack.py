import asyncio
from lib.async import async_wrapper
from lib.object import Object
from lib.message import Message

class Slack(object):
    class SlackError(Exception):
        pass

    def __init__(self):
        self._listeners = {}
        self._transforms = {}
        self._loop = None

        self.transform('message', self._transform_message)

    ########################################
    # BUILT-IN TRANSFORMATIONS
    ########################################

    def _transform_message(self, message):
        return Message(this._loop, this._client, message)

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    async def user_by_id(self, uid):
        resp = await async_wrapper(self._loop, self._client.api_call, 'users.list')

        if not api['ok']:
            raise SlackError('Unable to get user with ID {}.'.format(uid))
        
        for user in resp['users']:
            if user.get('id', -1) == uid:
                return user
        
        return None

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    async def _read(self):
        while True: 
            rtm_output = await async_wrapper(self._loop, self._client.rtm_read)
        
            if not rtm_output or len(rtm_output) == 0:
                continue

            yield [Object(line) for line in rtm_output]

    def on(self, evt, fn):
        if evt in self._listeners:
            self._listeners[evt].append(fn)
        else:
            self._listeners[evt] = [fn]

    def transform(self, evt, fn):
        self._transforms[evt] = fn

    async def listen(self):
        if not self._client.rtm_connect():
            print('Failed to connect to Slack RTM.')
            return

        async for output in self._read():
            for line in output:
                if line.type in self._listeners:
                    if line.type in self._transforms:
                        line = self._transforms[line.type](line)

                    for fn in self._listeners:
                        await fn(line)