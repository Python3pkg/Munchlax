import sys

sys.dont_write_bytecode = True

from ru import ru
from lib.secrets import secrets

ru.start(secrets.bot_oauth_token, '~')