import pickle, os, datetime
import discord

file_path = "cat.walks"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

allowed_mentions = discord.AllowedMentions()
allowed_mentions.everyone = False
allowed_mentions.roles = False
allowed_mentions.users = False


servers = []
class CatwalkServer:
    id = None
    server_name = None
    home_channel_name = None
    home_channel = None

    def __init__(self, id, server_name, home_channel_name, home_channel):
        self.id = id
        self.server_name = server_name
        self.home_channel_name = home_channel_name
        self.home_channel = home_channel


rooms = []
class CatwalkRoom:
    room_name = None
    servers = []

    def __init__(self, room_name, servers):
        self.room_name = room_name
        self.servers = servers


def load_data():
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            load_servers, load_rooms = pickle.load(file)

        return load_servers, load_rooms
    
    return [], []


    
def make_embed(message, roomname):
    embed = discord.Embed(description=message.content,
                      colour=0x00b0f4,
                      timestamp=datetime.datetime.now())

    embed.set_author(name=message.author,
                    icon_url=message.author.avatar.url)

    if len(message.stickers) > 0:
        embed.set_thumbnail(url=message.stickers[0].url)

    if len(message.attachments) > 0:
        embed.set_image(url=message.attachments[0].url)


    embed.set_footer(text=f"{message.author}@{message.guild.name} ({roomname})")

    return embed

def save_data():
    with open(file_path, 'wb') as file:
        pickle.dump((servers, rooms), file)

def check_server_exists(message):
    for catwalkServer in servers:
        if (catwalkServer.id == message.guild.id):
            return catwalkServer
        
    newCatwalkServer = CatwalkServer(message.guild.id, message.guild.name, None, None)
    servers.append(newCatwalkServer)
    return newCatwalkServer
    
def in_home_channel(message):
    for catwalkServer in servers:
        if catwalkServer.id == message.guild.id and catwalkServer.home_channel == message.channel.id:
            return True
    return False

def set_home_channel(message):
    for catwalkServer in servers:
        if catwalkServer.id == message.guild.id:
            catwalkServer.home_channel = message.channel.id
            catwalkServer.home_channel_name = message.channel.name

def remove_prefix(str, prefix):
    return str.removeprefix(prefix)

async def join_group(message, myServer, roomname):

    if not in_home_channel(message):
        await message.channel.send(f"Please, set up a home channel with 'Here, catwalk' first!")
        return

    for room in rooms: # Look through the rooms
        print (room)
        print (room.room_name)

        if room.room_name == roomname: # Found the room I was looking for

            for server in room.servers: # Look through the servers in that room
                if server.id == myServer.id: # Found myself
                    await message.channel.send(f"I'm already in the Catwalk room {roomname}!")
                    print("already joined")
                    return
            
            room.servers.append(myServer)

            serverList = ""
            for s in room.servers:
                serverList += "\n" + s.server_name

            await message.channel.send(f'I joined the Catwalk room {roomname}! This room hosts these servers: {serverList} :3')
            print("Didn't find myself. Added.")
            save_data()
            return
        
    await message.channel.send("I couldn't find that Catwalk room. You can create one saying 'Catwalk, create <Your room name here>' :3")
    print ("Didn't find that room")
    return

async def create_group(message, myServer, roomname):
    print("I created: "+roomname)
    roomFound = False

    if not in_home_channel(message):
        await message.channel.send(f"Please, set up a home channel with 'Here, catwalk' first!")
        return
    
    for room in rooms: # Look through the rooms
        if room.room_name == roomname: # Found a room with this name
            await message.channel.send(f"Sorry, a room with the name {roomname} already exists! Please try again!")
            print("taken")
            return
        
    newRoom = CatwalkRoom(roomname, [myServer])
    rooms.append(newRoom)

    await message.channel.send(f"Ok! :3 I created the room {roomname} Feel free to invite others!")
    save_data()
    print("created")
    return


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_guild_join(guild):
    print(f"Joined Guild: {guild.name}")
    print(f"Guild ID: {guild.id}")

@client.event
async def on_message(message):

    if message.author == client.user:
        return
    
    myServer = check_server_exists(message)

    if message.author.guild_permissions.manage_guild: # Mods only commands

        if message.content.lower().startswith('catwalk, here'):
            set_home_channel(message)
            await message.channel.send('Hi! I will be using this channel to communicate from here on out :3')
            return
        
        if message.content.lower().startswith('catwalk, join '): # Joining groups
            roomname = remove_prefix(message.content.lower(), 'catwalk, join ')

            await join_group(message, myServer, roomname)
            return
        
        if message.content.lower().startswith('catwalk, create '): #Creating groups
            roomname = remove_prefix(message.content.lower(), 'catwalk, create ')

            await create_group(message, myServer, roomname)
            return
        
        if message.content.lower().startswith('catwalk, setup '): #Creating groups
            roomname = remove_prefix(message.content.lower(), 'catwalk, setup ')

            set_home_channel(message)
            await create_group(message, myServer, roomname)
            await join_group(message, myServer, roomname)
            return
    

    if in_home_channel(message):

        print(f"Got a message {message.content} from {message.author} on channel {message.channel.id}")

        if (message.content.startswith('Catwalk!')):
            await message.channel.send(f'Hello, {message.author}!')

        for room in rooms:
            if myServer in room.servers:
                for s in room.servers:
                    target_guild = client.get_guild(s.id)
                    target_channel = target_guild.get_channel(s.home_channel)

                    if target_channel is not None and s.id is not myServer.id:
                        if len(message.stickers) > 0 or len(message.attachments) > 0:
                            await target_channel.send(embed=make_embed(message, room.room_name), allowed_mentions=allowed_mentions)
                        else:
                            await target_channel.send(f'{message.author}@{message.guild.name}: {message.content}', allowed_mentions=allowed_mentions) 
                        

        return
    
servers, rooms = load_data()

print (servers)
for s in servers:
    print (f"server {s.id} name {s.server_name} has a home channel {s.home_channel}")

print (rooms)

with open('token') as f:
    token = f.readline()
    client.run(token)