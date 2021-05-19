import discord
import asyncio
import random
from datetime import datetime
import os
from discord.ext import tasks
import json
import cloudfunctions as func
from itertools import cycle
from dotenv import load_dotenv

load_dotenv()
client = discord.Client()
ready = False
data = None
with open("data.json") as a:
    data = json.load(a)
botStatus = cycle(data["status"])
drop = []
server = None

@client.event
async def on_ready():
    global ready, server
    func.getBot(client)
    changeStat.start()
    server = await client.fetch_guild(821763643652833351)
    print("{0} successfully logged in!".format(client.user.name))
    ready = True
    return

@client.event
async def on_message(message):
    global drop
    if ready and not message.author.bot:
        command = func.splitCommand(message.content)
        if command:
            if command[0] == "help":
                await message.reply(embed=func.helpCommand(command))
                return
            if command[0] == "ping":
                await message.reply(content="Pong! {0}ms!".format(str(client.latency*1000).split(".")[0]))
                return
            if command[0] == "shop":
                await message.reply("This command is WIP. Please wait until Tata finishes it!", delete_after=10.0)
                return
            if command[0] in ["balance", "bal", "money"]:
                money = 0
                if len(command) == 1:
                    command.append(str(message.author.id))
                if command[1] in data["money"]:
                    money = data["money"][command[1]]
                embed = discord.Embed(description="You currently have {0} <:IC_PotCoin:843136980178436167>".format(money), colour=0x5abef0)
                await message.reply(embed=embed)
                return
            if [a for a in message.author.roles if a.id in data["modRoles"]] or message.author.guild_permissions.administrator:
                if command[0] == "modrole":
                    if len(command) == 1:
                        roles = "\n"
                        for each in data["modRoles"]:
                            role = server.get_role(each)
                            roles += "`{0}` ({1})\n".format(role.name, each)
                        await message.reply(content="All the modroles:"+roles)
                        return
                    if command[1] == "add" or command[1] == "new":
                        if len(command) == 2:
                            await message.reply(content="Please provide me a role! (using ID)")
                        roles = ""
                        for each in command[2:]:
                            id = int(func.mentionToID(each))
                            role = server.get_role(id)
                            if role != None:
                                roles += "`" + role.name + "` "
                            else:
                                continue
                            if id not in data["modRoles"]:
                                data["modRoles"].append(id)
                        func.updateData(data)
                        await message.reply(content="Successfully added roles below to modrole list!\n{0}".format(roles))
                        return
                    if command[1] in ["del", "delete", "remove"]:
                        if len(command) == 2:
                            await message.reply(content="Please provide me a role! (using ID)")
                        roles = ""
                        id = int(func.mentionToID(command[2]))
                        if id in data["modRoles"]:
                            data["modRoles"].remove(id)
                            func.updateData(data)
                            await message.reply(content="Successfully removed `{0}` from modrole list!\n".format(server.get_role(id).name))
                            return
                        await message.reply(content="`{0}` is a invalid role".format(command[2]))
                    await message.reply(content="modrole command has no subcommand: `{0}`".format(command[1]))
                if command[0] == "status":
                    if len(command) == 1:
                        statuses = "\n"
                        for each in range(len(data["status"])):
                            statuses += "({0}) `{1}`\n".format(each, data["status"][each])
                        await message.reply(content="All the statuses:"+statuses)
                        return
                    if command[1] == "add" or command[1] == "new":
                        if len(command) == 2:
                            await message.reply(content="Please provide me a new status!")
                        statuses = ""
                        for each in command[2:]:
                            if each not in data["status"]:
                                statuses += "`{0}`\n".format(each)
                                data["status"].append(each)
                        func.updateData(data)
                        await message.reply(content="Successfully added status below to status list!\n{0}".format(statuses))
                        return
                    if command[1] in ["del", "delete", "remove"]:
                        if len(command) == 2 or not command[2].isnumeric():
                            await message.reply(content="Please provide me the index of the status!")
                        if int(command[2]) < len(data["status"]):
                            statuses = data["status"].pop(int(command[2]))
                            func.updateData(data)
                            await message.reply(content="Successfully removed `{0}` from modrole list!\n".format(statuses))
                            return
                    await message.reply(content="status command has no subcommand: `{0}`".format(command[1]))
                if command[0] == "dropchannel":
                    if len(command) == 1:
                        channels = "\n"
                        for each in data["dropChannel"]:
                            channel = await client.fetch_channel(each)
                            channels += "`#{0}` ({1})\n".format(channel.name, each)
                        await message.reply(content="All the drop channels:"+channels)
                        return
                    if command[1] == "add" or command[1] == "new":
                        if len(command) == 2:
                            await message.reply(content="Please provide me a new channel! (using ID)")
                        channels = ""
                        for each in command[2:]:
                            id = int(func.mentionToID(each))
                            channel = await client.fetch_channel(id)
                            if channel != None:
                                channels += "`#" + channel.name + "` "
                            else:
                                continue
                            if id not in data["dropChannel"]:
                                data["dropChannel"].append(id)
                        func.updateData(data)
                        await message.reply(content="Successfully added channels below to dropchannel list!\n{0}".format(channels))
                        return
                    if command[1] in ["del", "delete", "remove"]:
                        if len(command) == 2:
                            await message.reply(content="Please provide me a channel! (using ID)")
                        channels = ""
                        id = int(func.mentionToID(command[2]))
                        if id in data["dropChannel"]:
                            data["dropChannel"].remove(id)
                            func.updateData(data)
                            await message.reply(content="Successfully removed `{0}` from dropchannel list!\n".format((await client.fetch_channel(id)).name))
                            return
                        await message.reply(content="`{0}` is a invalid channel".format(command[2]))
                    await message.reply(content="dropchannel command has no subcommand: `{0}`".format(command[1]))
                if command[0] == "newdrop":
                    if len(command) == 1:
                        command.append(random.randint(100, 999))
                    elif not command[1].isnumeric():
                        command[1] == command.append(random.randint(100, 999))
                    if len(command) == 2:
                        command.append(message.channel.id)
                    else:
                        try:
                            command[2] = (await client.fetch_channel(func.mentionToID(command[2]))).id
                        except:
                            command[2] = message.channel.id
                    if len(command) == 3:
                        command.append(func.generatePassword(4))
                    elif command[3].isnumeric() and int(command[3])<30:
                        command[3] = func.generatePassword(command[3])
                    else:
                        command[3] = message.content[message.content.lower().find(command[3]):]
                    drop = await func.cleanDrop(drop)
                    channel = await client.fetch_channel(command[2])
                    drop.append(int(command[1]))
                    drop.append(command[3])
                    embed = discord.Embed(title="Pot Coin Drop!", colour=0x5abef0, description="type `{0}` to earn {1} <:IC_PotsuCoin:843136980178436167>!".format(drop[1], str(drop[0])))
                    drop.append(await channel.send(content=func.idToMention(message.author.id), embed=embed))
                    await asyncio.sleep(60)
                    await func.cleanDrop(drop)
                    return
        if message.channel.id in data["dropChannel"]:
            if not (random.randint(0,20) or drop):
                drop.append(random.randint(100, 999))
                drop.append(func.generatePassword(4))
                embed = discord.Embed(title="Pot Coin Drop!", colour=0x5abef0)
                embed.description = "type `{0}` to earn {1} <:IC_PotsuCoin:843136980178436167>!".format(drop[1], str(drop[0]))
                drop.append(await message.channel.send(embed=embed))
                await asyncio.sleep(60)
                await func.cleanDrop(drop)
                return
        if drop and drop[2].channel.id == message.channel.id and message.content.lower() == drop[1]:
            drop[1] = ""
            channel = message.channel
            user    = message.author
            userID  = str(user.id)
            sum = drop[0]
            if userID in data:
                sum += data["money"][userID]
            data["money"].update({userID:sum})
            func.updateData(data)
            await channel.send(content="{0} has earnt {1} <:IC_PotsuCoin:843136980178436167> from random drop!".format(func.idToMention(userID), str(drop[0])), delete_after=5.0)
            
            drop = await func.cleanDrop(drop)
            await message.delete()
            return
        if message.author.id == 301270165222588417:
            if message.content == "cloudbot fuck off":
                await message.add_reaction(r"✅")
                await client.close()
    return

@tasks.loop(seconds=30)
async def changeStat():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next(botStatus)), status=discord.Status.idle)

client.run(os.getenv("TOKEN"), bot=True)
print("Bot closed.")
