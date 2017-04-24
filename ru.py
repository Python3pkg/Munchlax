from datetime import datetime
from slackru import SlackRU
from lib import validators
from models.user import User
from models.request import Request

ru = SlackRU()

@ru.command(requires=[validators.is_mentor])
async def active(message):
    if not User.set_active(message.user.name, True):
        await message.reply('Unable to set your active status.')
        return

    await message.reply('Your status has been set to active.')

@ru.command(requires=[validators.is_mentor])
async def inactive(message):
    if not User.set_active(message.user.name, False):
        await message.reply('Unable to set your active status.')
        return

    await message.reply('Your status has been set to inactive.')

@ru.command(requires=[validators.is_mentor])
async def busy(message):
    if not User.set_busy(message.user.name, True):
        await message.reply('Unable to set your busy status.')
        return

    await message.reply('Your status has been set to busy.')

@ru.command(requires=[validators.is_mentor])
async def unbusy(message):
    if not User.set_busy(message.user.name, False):
        await message.reply('Unable to set your busy status.')
        return

    await message.reply('Your status has been set to unbusy.')

@ru.command(requires=[validators.is_mentor])
async def status(message):
    user = User.from_name(message.user.name)

    if user is None:
        await message.reply('You are not in the mentor database.')
        return

    await message.channel.write(
        attachments=[
            {
                'fallback': 'Active: {} / Busy: {}.'.format(user.is_active, user.is_busy),
                'author_name': user.slack,
                'fields': [
                    {
                        'title': 'Active',
                        'value': 'Yes' if user.is_active else 'No',
                        'short': True
                    },
                    {
                        'title': 'Busy',
                        'value': 'Yes' if user.is_busy else 'No',
                        'short': True
                    }
                ]
            }
        ]
    )

@ru.command()
async def mentors(message):
    Request.create(message.user, datetime.utcnow(), message.text)
    
    # Write an interactive message to Slack where "Yes" posts to a hook
    # to remove the request and pair. "No" does nothing.
    # https://api.slack.com/docs/message-buttons

@ru.command(cmd='setchannel', requires=[validators.is_mentor])
async def set_mentor_channel(message):
    ru.mentor_channel = message.channel.id
    await message.reply('Mentor messages have been set to be posted in this channel.')