from bot import Bot
import validators

ru = Bot()

@ru.command(requires=[validators.is_mentor])
def active(message):
    pass

@ru.command(requires=[validators.is_mentor])
def inactive(message):
    pass

@ru.command(requires=[validators.is_mentor])
def busy(message):
    pass

@ru.command(requires=[validators.is_mentor])
def unbusy(message):
    pass

@ru.command(requires=[validators.is_staff])
def status(message):
    pass