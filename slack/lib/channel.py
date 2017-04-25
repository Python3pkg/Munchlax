from .method import build_methods

class Channel(object):
    methods = {
        'archive': 'channels.archive',
        'get_history': 'channels.history', # Replace with hand-written code.
        'invite': 'channels.invite',
        'kick_user': 'channels.kick',
        'join': 'channels.join',
        'leave': 'channels.leave',
        'rename': 'channels.rename',
        'set_purpose': 'channels.setPurpose',
        'set_topic': 'channels.setTopic',
        'unarchive': 'channels.unarchive',
        'invite': 'channels.invite',
        'upload': 'files.upload'
    }

    def __init__(self, loop, client, channel):
        self.__dict__.update(channel.__dict__)
        self._loop = loop
        self._client = client

        build_methods(self, {
            'channel': self.id,
            'channels': self.id
        })