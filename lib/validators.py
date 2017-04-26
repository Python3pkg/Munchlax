from models.user import User

async def is_mentor(message):
    user = await message.get_author()
    return User.is_mentor(user.name)