from .method import build_methods

class Message(object):
    methods = {
        'reply': 'chat.postMessage',
        'upload_reply': 'files.upload',
        'delete': 'chat.delete',
        'add_reaction': 'reactions.add',
        'get_reactions': 'reactions.get', # Replace with hand-written code.
        'remove_reaction': 'reactions.remove',
        'get_channel_replies': 'channels.replies', # Replace with hand-written code.
        'get_group_replies': 'groups.replies' # Replace with hand-written code.
    }

    def __init__(self, loop, client, message):
        self.__dict__.update(message.__dict__)
        self._loop = loop
        self._client = client

        build_methods(self, {
            'channel': self.channel,
            'timestamp': self.ts,
            'thread_ts': self.ts
        })

    async def get_author(self):
        if getattr(self, 'user', None) is not None:
            return await self._client.user_from_id(self.user)
        elif getattr(self, 'bot_id', None) is not None:
            return await self._client.bot_from_id(self.bot_id)

    async def get_channel(self):        
        if getattr(self, 'channel', None) is not None:
            return await self._client.channel_from_id(self.channel)
        elif getattr(self, 'group', None) is not None:
            return await self._client.channel_from_id(self.group)