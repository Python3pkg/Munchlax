from .list import List
from .object import Object

class File(Object):
    def __init__(self, slack, file):
        Object.__init__(self, file)
        self._slack = slack

    async def get_channels(self):
        i = 0

        def next():
            if len(self.channels) <= i:
                return None
            channel = await self._slack.channel_by_id(self.channels[i])
            i += 1
            return channel

        return List(next)

    async def share(self):
        return await self._slack.share_file(self)

    async def revoke(self):
        return await self._slack.revoke_file(self)

    async def delete(self):
        return await self._slack.delete_file(self)

    async def get_comments(self, **kwargs):
        return await self._slack.get_file_comments(self, **kwargs)

    async def comment(self, comment):
        return await self._slack.add_file_comment(self, comment)

    async def add_reaction(self, name):
        return await self._slack.add_file_reaction(self, name)

    async def get_reactions(self):
        return await self._slack.get_file_reactions(self)

    async def remove_reaction(self, name):
        return await self._slack.remove_file_reaction(self, name)