import asyncio
from datetime import datetime, timedelta
import json
from slackclient import SlackClient
from lib.async import async_wrapper
from lib.object import Object
from lib.message import Message
from lib.channel import Channel
from lib.group import Group
from lib.user import User

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

    async def _transform_message(self, message):
        message = Message(self._loop, self._client, message)

        if getattr(message, 'user', None) is not None:
            message.user = await self.user_from_id(message.user)
        elif getattr(message, 'bot_id', None) is not None:
            message.bot = await self.bot_from_id(message.bot_id)
        
        if getattr(message, 'channel', None) is not None:
            message.channel = await self.channel_from_id(message.channel)

        if getattr(message, 'group', None) is not None:
            message.group = await self.channel_from_id(message.group)

        return message

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    async def channel_from_id(self, id):
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.info',
            channel=id
        )

        if channel is not None and channel['ok']:
            return Channel(self._loop, self._client, Object(channel['channel']))

        return None

    async def group_from_id(self, id):
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.info',
            group=id
        )

        if group is not None and group['ok']:
            return Group(self._loop, self._client, Object(group['group']))

        return None

    async def user_from_id(self, uid):
        user = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.info',
            user=uid
        )

        if user is not None and user['ok']:
            return User(self._loop, self._client, Object(user['user']))
        
        return None

    async def bot_from_id(self, bid):
        bot = await async_wrapper(
            self._loop,
            self._client.api_call,
            'bot.info',
            bot=bid
        )

        if bot is not None and bot['ok']:
            return User(self._loop, self._client, Object(user['bot']))
        
        return None

    ########################################
    # UTILITY FUNCTIONS
    ########################################

    def _format_timestamp(self, ms):
        epoch = datetime(1970, 1, 1)
        return epoch + timedelta(seconds=ms)

    async def _read(self):
        while True: 
            rtm_output = await async_wrapper(self._loop, self._client.rtm_read)

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

        startup = datetime.utcnow()

        async for output in self._read():
            for line in output:
                # Convert Slack timestamps to datetime objects.
                if getattr(line, 'ts', None) is not None:
                    line.ts = self._format_timestamp(float(line.ts))

                    # ignore messages from the past.
                    if line.ts < startup:
                        continue

                if line.type in self._listeners:
                    if line.type in self._transforms:
                        line = await self._transforms[line.type](line)

                    for fn in self._listeners[line.type]:
                        await fn(line)

    def set_token(self, token):
        self._client = SlackClient(token)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())