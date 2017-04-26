from .object import Object

class Channel(Object):
    def __init__(self, slack, channel):
        Object.__init__(self, channel)
        self._slack = slack

    async def write(self, text, **kwargs):
        return await self._slack.raw_write(self.id, text=text, **kwargs)

    async def upload(self, **kwargs):
        return await self._slack.upload_file(self, **kwargs)

    async def get_history(self, **kwargs):
        return await self._slack.get_channel_history(self, **kwargs)

    async def archive(self):
        return await self._slack.archive_channel(self)

    async def invite_user(self, user):
        return await self._slack.archive_channel(self, user)

    async def join(self, validate=False):
        return await self._slack.join_channel(self, validate=validate)

    async def kick_user(self, user):
        return await self._slack.channel_kick(self, user)

    async def leave(self):
        return await self._slack.leave_channel(self)

    async def mark(self, ts):
        return await self._slack.mark_channel(self, ts)

    async def rename(self, name, validate=False):
        channel = await self._slack.rename_channel(self, name, validate=validate)
        self.__dict__.update(channel.__dict__)
        return self

    async def get_replies(self, ts):
        replies = await self._slack.get_channel_replies(self, ts)
        return replies

    async def set_purpose(self, purpose):
        """
        Sets the purpose for a channel.
        This causes the _Channel_ object being worked on
        to become stale.

        Args:
            purpose: The purpose to use when updating the channel.

        Returns:
            The new purpose of the channel.

        Raises:
            SlackError: This is raised if the "ok" property of
                Slack's response is not True.
        """
        return await self._slack.set_channel_purpose(self, purpose)

    async def set_topic(self, topic):
        return await self._slack.set_channel_topic(self, topic)

    async def list_members(self):
        all_users = await self._client.list_users()
        all_users = [User(x) for x in all_users]
        return [x for x in all_users if x.id in self.members] 

    async def update(self):
        """
        Updates the current _Channel_ object.
        There isn't much benefit to using this and it's here
        if you don't want to replace your current _Channel_ object
        or can't.

        Raises:
            SlackError: This is raised if the "ok" property of
                Slack's response is not True.
        """
        updated_copy = self._slack.channel_by_id(self.id)
        self.__dict__.update(updated_copy.__dict__)