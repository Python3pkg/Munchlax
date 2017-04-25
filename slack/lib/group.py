from .method import build_methods

class Group(object):
    methods = {
        'close': 'groups.close',
        'create': 'groups.create',
        'createChild': 'groups.createChild',
        'get_history': 'groups.history', # Replace with hand-written code.
        'invite': 'groups.invite',
        'kick': 'groups.kick',
        'leave': 'groups.leave',
        'rename': 'groups.rename',
        'set_purpose': 'groups.setPurpose',
        'set_topic': 'groups.setTopic',
        'unarchive': 'groups.unarchive',
        'upload': 'files.upload'
    }

    def __init__(self, loop, client, group):
        self.__dict__.update(group.__dict__)
        self._loop = loop
        self._client = client

        build_methods(self, {
            'channel': self.id,
            'channels': self.id
        })

    async def list_members(self):
        all_users = await self._client.list_users()
        all_users = [User(x) for x in all_users]
        return [x for x in all_users if x.id in self.members]