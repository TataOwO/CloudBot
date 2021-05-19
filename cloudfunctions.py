import json
from discord import Embed
import random

client = None

def idToMention(id):
    return "<@!"+str(id)+">"

def mentionToID(mention):
    if mention.isnumeric():
        return mention
    if len(mention)>=22 and mention[3:21].isnumeric():
        return mention[3:21]
    if len(mention)>=21 and mention[2:20].isnumeric():
        return mention[2:20]
    return False

def splitCommand(command):
    command = command.split(" ")
    if mentionToID(command[0]) == str(client.user.id):
        return command[1:]
    try:
        if command[0][:2] == "c!" and command[0]!="c!":
            command[0] = command[0][2:]
            return command
    except:
        return False
    return False

def getBot(inp):
    global client
    client = inp
    return

def updateData(data):
    with open("data.json", "w") as a:
        a.write(json.dumps(data, indent=4))
    return

def generatePassword(count):
    password = ""
    for a in range(int(count)):
        password += chr(random.randint(97, 122))
    return password

async def cleanDrop(drop):
    if drop:
        try:
            await drop[2].delete()
        except:
            drop = []
    return []

def helpCommand(command):
    embed = Embed(colour=0x5abef0)
    if len(command)==1:
        embed.title = "Cloud Bot Help Commands"
        embed.add_field(name="Utility", value="`help` `ping`")
        embed.add_field(name="Economy", value="`shop` `balance`")
        embed.add_field(name="Mod Only",value="`modrole` `status` `dropchannel` `newdrop`")
        return embed
    if command[1] == "help":
        embed = helpCommand(["help"])
        embed.description = "So you asked how to use help command... but why?"
        embed.add_field(name="Usage", value="```css\nc!help [command]```")
        return embed
    if command[1] == "ping":
        embed.title = "Ping"
        embed.description = "Shows the bot latency in millisecond."
        embed.add_field(name="Usage", value="```css\nc!ping```")
        return embed
    if command[1] == "shop":
        embed.title = "Shop"
        embed.description = "This command is WIP."
        return embed
    if command[1] in ["balance", "bal", "money"]:
        embed.title = "Balance"
        embed.description = "Shows how many coins a user has."
        embed.add_field(name="Alias", value="`balance` `bal` `money`")
        embed.add_field(name="Usage", value="```css\nc!balance [user]```")
        return embed
    if command[1] == "modrole":
        if len(command) == 2:
            embed.title = "Modrole"
            embed.description = "Shows a list of modroles."
            embed.add_field(name="Subcommands", value="`add` `del`")
            embed.add_field(name="Usage", value="```css\nc!modrole (add, del)```")
            return embed
        if command[2] == "add":
            embed.title = "Modrole add"
            embed.description = "Add roles to the modrole list."
            embed.add_field(name="Usage", value="```css\nc!modrole add [role ID 1] [role ID 2]...```")
            return embed
        if command[2] in ["del", "delete", "remove"]:
            embed.title = "Modrole delete"
            embed.description = "Remove a role from the modrole list.\n"
            embed.add_field(name="Alias", value="`del` `delete` `remove`")
            embed.add_field(name="Usage", value="```css\nc!modrole del [role ID]```")
            return embed
    if command[1] == "status":
        if len(command) == 2:
            embed.title = "Status"
            embed.description = "Shows a list of statuses."
            embed.add_field(name="Subcommands", value="`add` `del`")
            embed.add_field(name="Usage", value="```css\nc!status (add, del)```")
            return embed
        if command[2] == "add":
            embed.title = "Status add"
            embed.description = "Add a new status to the status list."
            embed.add_field(name="Usage", value="```css\nc!status add [text]```")
            return embed
        if command[2] in ["del", "delete", "remove"]:
            embed.title = "Status delete"
            embed.description = "Remove a status from the status list.\nMake sure to check the index of the status you want to delete."
            embed.add_field(name="Alias", value="`del` `delete` `remove`")
            embed.add_field(name="Usage", value="```css\nc!status del [index]```")
            return embed
    if command[1] == "dropchannel":
        if len(command) == 2:
            embed.title = "Dropchannel"
            embed.description = "Shows a list of channels that do random drops."
            embed.add_field(name="Subcommands", value="`add` `del`")
            embed.add_field(name="Usage", value="```css\nc!dropchannel (add, del)```")
            return embed
        if command[2] == "add":
            embed.title = "Dropchannel add"
            embed.description = "Add a channel to the dropchannel list."
            embed.add_field(name="Usage", value="```css\nc!dropchannel add [channel ID 1] [channel ID 2]...```")
            return embed
        if command[2] in ["del", "delete", "remove"]:
            embed.title = "Dropchannel delete"
            embed.description = "Remove a channel from the dropchannel list."
            embed.add_field(name="Alias", value="`del` `delete` `remove`")
            embed.add_field(name="Usage", value="```css\nc!dropchannel del [channel ID]```")
            return embed
    if command[1] == "newdrop":
        embed.title = "New Drop"
        embed.description = "Create a new drop to a channel."
        embed.add_field(name="Usage", value="```css\nc!newdrop [coin count] [channel ID] [password]```")
        return embed
    a = "`"
    for each in command:
        a += each + " "
    a = a[:len(a)-1]+"`"
    embed.title = "Sorry, I could not find this command:"
    embed.description = a
    return embed

