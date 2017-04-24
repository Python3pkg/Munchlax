from models.user import User

def is_mentor(message):
    return User.is_mentor(message.user.name)