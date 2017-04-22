import asyncio
from shlex import shlex

READ_WEBSOCKET_DElAY = 1
MAX_MESSAGE_LENGTH = 1000

class Slack(object):
    class SlackError(Exception):
        pass

    async def _user_by_id(self, uid):
        resp = await self.slack_client.api_call('users.list')

        if(!api['ok']):
            raise SlackError('Unable to get user with ID {}.'.format(uid))
        
        for user in resp['users']:
            if user.get('id', -1) == uid:
                return user
        
        return None

    async def _read(self):
        AT_BOT = '<@' + self.UID + '>'
        
        rtm_output = await self.slack_client.rtm_read()
    
        if not rtm_output or len(rtm_output) == 0:
            return

        for output in rtm_output:
            if output and 'text' in output and AT_BOT in output['text']:
                yield output

    def _parse(line):
        '''
        Tokenizes a string _line_ and returns a list of tokens.
        Tokens are whitespace delimited.
        '''
        tokens = shlex(line, posix=True)
        tokens.whitespace_split = True

        ret = []
        token = tokens.get_token()
        
        while token is not None:
            ret.append(token)
            token = tokens.get_token()

        return ret

    async def listen(self):
        if !slack_client.rtm_connect():
            print('Connection failed. Invalid Slack token or bot ID?')
            return

        print('Slack bot is now running.')

        while True:
            output = self._read()

            for line in output:
                if len(line['text']) > MAX_MESSAGE_LENGTH:
                    continue

                command = self._parse(line)
                await self._commands.apply(command)

            asyncio.sleep(READ_WEBSOCKET_DELAY)