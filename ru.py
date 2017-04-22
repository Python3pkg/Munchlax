from bot import Bot
import validators

ru = Bot()

@ru.command(requires=[validators.is_mentor])
async def active(message):
    pass

@ru.command(requires=[validators.is_mentor])
async def inactive(message):
    pass

@ru.command(requires=[validators.is_mentor])
async def busy(message):
    pass

@ru.command(requires=[validators.is_mentor])
async def unbusy(message):
    pass