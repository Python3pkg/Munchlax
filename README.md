# Slack Bot

A Python-based Slack bot written with concurrency in mind.

## Features

- Easily extensible through an easy to use `command` decorator

## Install

```
pip install munchlax
```

## Method List

- [ ] API
- [ ] Auth
- [ ] Bots
- [x] Channels
- [x] Chat (missing **me** and **unfurl**)
- [ ] DND
- [ ] Emoji
- [x] Files.Comments
- [x] Files
- [X] Groups
- [X] IM
- [X] MPIM
- [ ] Oauth
- [ ] Pins
- [X] Reactions (missing support for file comments as well as **list**)
- [ ] Reminders
- [x] RTM (Will not Implement)
- [ ] Search
- [ ] Stars
- [ ] Team
- [ ] Team.Profile
- [ ] Usergroups
- [ ] Usergroups.Users
- [ ] Users
- [ ] Users.Profile

## Tips

- Anything that modifies Slack object state will cause library objects to become stale. You should remember to update any modified objects by calling `<Object>#update`. The only exception to this is the method `Message#edit`. This method call will automatically update the associated `Message` object.