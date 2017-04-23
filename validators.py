from lib.stack import get_internal
from models.user import User

def is_mentor():
    message = get_internal('message')
    return User.is_mentor(message.user.name)