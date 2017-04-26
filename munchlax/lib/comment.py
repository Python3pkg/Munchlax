from .object import Object

class Comment(Object):
    def __init__(self, slack, comment, file):
        Object.__init__(self, comment)
        self._slack = slack
        self._file = file

    async def delete(self):
        return await self._slack.delete_comment(self._file, self)

    async def edit(self, comment):
        return await self._slack.edit_comment(self._file, self, comment)