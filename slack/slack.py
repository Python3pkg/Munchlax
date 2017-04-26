import asyncio
from datetime import datetime, timedelta
import json
from slackclient import SlackClient
from .lib.async import async_wrapper
from .lib.object import Object
from .lib.message import Message
from .lib.channel import Channel
from .lib.group import Group
from .lib.user import User
from .lib.slackerror import SlackError

class Slack(object):
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
        return Message(self, message)

    ########################################
    # SLACK METHODS
    ########################################

    async def channel_from_id(self, id):
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.info',
            channel=id
        )

        if channel['ok']:
            return Channel(self, channel['channel'])

        raise SlackError(channel['error'])

    async def group_from_id(self, id):
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.info',
            group=id
        )

        if group['ok']:
            return Group(self, group['group'])

        raise SlackError(channel['error'])

    async def user_from_id(self, uid):
        user = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.info',
            user=uid
        )

        if user['ok']:
            return User(self, user['user'])
        
        raise SlackError(user['error'])

    async def bot_from_id(self, bid):
        bot = await async_wrapper(
            self._loop,
            self._client.api_call,
            'bot.info',
            bot=bid
        )

        if bot['ok']:
            return Bot(self, bot['bot'])
        
        raise SlackError(bot['error'])

    async def create_channel(self, name, validate=False):
        channel = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.create',
            name=name,
            validate=validate
        )

        if channel['ok']:
            return Channel(self, channel['channel'])
        
        raise SlackError(channel['error'])

    async def create_group(self, name, validate=False):
        group = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.create',
            name=name,
            validate=validate
        )

        if group['ok']:
            return Channel(self, group['group'])

        raise SlackError(group['error'])

    async def list_channels(self, exclude_archived=False):
        channels = await async_wrapper(
            self._loop,
            self._client.api_call,
            'channels.list',
            exclude_archived=exclude_archived
        )

        if channels['ok']:
            return [Channel(self, x) for x in channels['channels']]

        raise SlackError(channels['error'])

    async def list_groups(self, exclude_archived=False):
        groups = await async_wrapper(
            self._loop,
            self._client.api_call,
            'groups.list',
            exclude_archived=exclude_archived
        )

        if groups['ok']:
            return [Group(self, x) for x in groups['groups']]

        raise SlackError(groups['error'])

    async def list_users(self, presence=True):
        users = await async_wrapper(
            self._loop,
            self._client.api_call,
            'users.list',
            presence=presence
        )
        
        if users['ok']:
            return [User(self, x) for x in users['members']]
        
        raise SlackError(users.users)

    async def whoami(self):
        me = await async_wrapper(
            self._loop,
            self._client.api_call,
            'auth.test'
        )

        if me['ok']:
            return Object(me)
        
        raise SlackError(me['error'])

    async def write(self, **kwargs):
        resp = await async_wrapper(
            self._loop,
            self._client.api_call,
            'chat.postMessage',
            **kwargs
        )

        if resp['ok']:
            return Message(self, resp['message'])
        
        raise SlackError(resp['error'])


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

            yield [line for line in rtm_output]

    def on(self, evt, fn):
        if evt in self._listeners:
            self._listeners[evt].append(fn)
        else:
            self._listeners[evt] = [fn]

    def transform(self, evt, fn):
        self._transforms[evt] = fn

    async def listen(self):
        self._loop = asyncio.get_event_loop()

        me = await self.whoami()
        self.uid = me.user_id

        print('Using user "{}" with ID {}.'.format(me.user, me.user_id))

        if not self._client.rtm_connect():
            print('Failed to connect to Slack RTM.')
            return

        print('Connected to Slack RTM.')

        startup = datetime.utcnow()

        async for output in self._read():
            for line in output:
                if line['type'] in self._listeners:
                    if line['type'] in self._transforms:
                        line = await self._transforms[line['type']](line)
                    else:
                        line = Object(line)

                    # Convert Slack timestamps to datetime objects.
                    if getattr(line, 'ts', None) is not None:
                        line.ts = self._format_timestamp(float(line.ts))

                        # ignore messages from the past.
                        if line.ts < startup:
                            continue

                    for fn in self._listeners[line.type]:
                        await fn(line)

    def set_token(self, token):
        self._client = SlackClient(token)

    def start(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.listen())