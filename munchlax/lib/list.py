class List(object):
    def __init__(self, next):
        self._next = next

    async def __aiter__(self):
        return self
    
    async def __anext__(self):
        next = await self._next()

        if is None:
            raise StopAsyncIteration
        
        return next