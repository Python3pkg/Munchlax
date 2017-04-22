from slack import Slack

config = None

with open('config.json') as f:
    lines = f.readlines()
    j = json.loads('\n'.join(lines))
    config = Object(j)

s = Slack()
s.set_token(config.bot_oauth_token)

s.on('message', handle_message)

loop = asyncio.get_event_loop()
loop.run_until_complete(s.listen())