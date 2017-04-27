from .list import List
from .object import Object

class File(Object):
    def __init__(self, slack, file):
        Object.__init__(self, file)
        self._slack = slack

    async def get_channels(self):
        """
        Fetches and returns an async iterator of all
        channels this file has been shared in.

        ```
        async for channel in file.get_channels():
            await channel.write('hello, world!')
        ```

        Returns:
            List<Channel>: An async iterator of all channels.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        i = 0

        def next():
            if len(self.channels) <= i:
                return None
            channel = await self._slack.channel_by_id(self.channels[i])
            i += 1
            return channel

        return List(next)

    async def share(self):
        """
        Creates a public URL for the file.

        This will cause the current `File` object to become stale.

        Returns:
            File: An updated `File` object with the public URL for
                the file.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.share_file(self)

    async def revoke(self):
        """
        Revokes the file from being shared publicly.

        This will cause the current `File` object o become stale.

        Returns:
            File: An updated `File` object without the public URL for
                the file.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.revoke_file(self)

    async def delete(self):
        """
        Deletes the file.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.delete_file(self)

    async def get_comments(self, count=100, page=1):
        """
        Fetches and returns the comments for the file.

        Args:
            count (int): The number of comments per page to return.

                Defaults to 100.
            page (int): The comments page number to use.

                Defaults to 1

        Returns:
            list<Comment>: A list of `Comment` objects for the query.
            object: A generic object containing paging information.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.get_file_comments(self, **kwargs)

    async def comment(self, comment):
        """
        Adds a comment to the file.

        Args:
            comment (str): The comment string.

        Returns:
            Comment: A `Comment` object representing the new comment.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.add_file_comment(self, comment)

    async def add_reaction(self, name):
        """
        Adds a reaction to the file.

        Args:
            name (str): The name of the reaction to add.

                A list of standard Slack reactions/emoji can be found at
                https://www.webpagefx.com/tools/emoji-cheat-sheet/
                
        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.add_file_reaction(self, name)

    async def get_reactions(self):
        """
        Fetches and returns a list of all reactions for the file.

        Returns:
            list<Object>: A list of generic objects with reaction data.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.get_file_reactions(self)

    async def remove_reaction(self, name):
        """
        Removes a reaction from the file.

        Args:
            name (str): The name of the reaction to remove.

        Raises:
            SlackError: Raised in the event that Slack does not return "ok".
        """
        return await self._slack.remove_file_reaction(self, name)