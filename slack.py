import asyncio
import json
from slackclient import SlackClient
from lib.async import async_wrapper
from lib.object import Object
from lib.message import Message
from lib.channel import Channel
from lib.group import Group

class Slack(object):
    class SlackError(Exception):
        pass

    def __init__(self):
        self._listeners = {}
        self._transforms = {}
        self._loop = None
        self._client = None

        self.transform('message', self._transform_message)

    ########################################
    # BUILT-IN TRANSFORMATIONS
    ########################################

    def _transform_message(self, message):
        return Message(self._loop, self._client, message)

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    async def channel_from_id(id):
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.info',
            channel=id
        )

        if channel['ok']:
            return Channel(self._loop, self._client, Object(channel))

        return None

    async def group_from_id(id):
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.info',
            channel
        )

        if group['ok']:
            return Group(self._loop, self._client, Object(channel))

        return None

    async def user_from_id(self, uid):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.info',
            user=uid
        )

        if api['ok']:
            return User(self._loop, self._client, Object(user))
        
        return None

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    def _read(self):
        while True: 
            rtm_output = self._client.rtm_read()

            if len(rtm_output) == 0:
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
        self._loop = asyncio.get_event_loop()

        if not self._client.rtm_connect():
            print('Failed to connect to Slack RTM.')
            return

        print('Connected to Slack RTM.')

        for output in self._read():
            for line in output:
                if line.type in self._listeners:
                    if line.type in self._transforms:
                        line = self._transforms[line.type](line)

                    for fn in self._listeners[line.type]:
                        await fn(line)

    def set_token(self, token):
        self._client = SlackClient(token)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())