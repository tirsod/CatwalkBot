# CatwalkBot
Group chats for Discord Guilds.

# Why
I'm in a lot of servers with many common members. This bot creates a "megachannel" that bridges those server groups together.
It connects you with people, it enables cross-server announcements, and it's easy to set up.

# How
Make a new discord application (https://discord.com/developers/docs/intro).


Create a file 'token' (no extension) and paste your token into it. Put it right next to the .py script.


Enable message content Intents


Get a OAuth invite link with message permissions (View, delete, manage, send stickers, links, embeds, etc)

Run the script (lol)

# Usage
Invite the bot to your server, visit the channel you wish the bot to use for communications and run:
```
Catwalk, here
Catwalk, create MyGroup
```
On the other servers you want to connect, you can run:
```
Catwalk, here
Catwalk, join MyGroup
```
or just run
```
Catwalk, setup MyGroup
```
and skip over the details.
(You need Manage Guild permissions to do this.)

# Features
This early version creates and joins groups, but has no way of leaving them.

It creates embeds when the messages include attachments or stickers.

No moderation tools (yet).

Serializes rooms and server connections using 'pickle'

# Requirements

Python 3

Discord.py

Your own 'token' file with your bot token inside.

Friends
