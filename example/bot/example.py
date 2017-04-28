import os
from munchlax.bot import Bot

bot = Bot()
bot.set_token('xoxp-173140984612-173910942023-173109891251-870792a47dc8a17727b1320a1c4eb441')
bot.set_prefix('~')

@bot.command()
async def hello(message):
    await message.reply('hi!')

async def is_even(x):
    arg = x.split(' ')[1]

    if not arg.isnumeric():
        return False

    return float(arg) % 2 == 0

@bot.command(requires=[lambda message: is_even(message.text)])
async def divide_even(message):
    """
    A command that responds to ``~divide_even 10.6``
    """
    number = float(message.text.split(' ')[1])
    await message.reply(str(number / 2))

bot.start()