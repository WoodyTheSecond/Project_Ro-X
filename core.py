import discord
import asyncio
import time
import os
import json
from discord.ext.commands import Bot
from discord.ext import commands
from itertools import cycle
import urllib.request
import random
import string
import sys

TOKEN = os.getenv("TOKEN")
client = commands.Bot(command_prefix=".")
client.remove_command("help")
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)
extensions = []


@client.event
async def on_ready():
    print("Bot is online.")
    await client.change_presence(game=discord.Game(name="Commands: .cmds"))


@client.event
async def on_member_join(member):
    server = member.server
    howtobuychannel = server.get_channel("457895087104327680")
    await client.send_message(member, "Welcome to **{}** if you want to buy the script read {}".format(server.name, howtobuychannel.mention))


async def isBotChannel(message: discord.Message, channel: discord.Channel):
    server = channel.server
    botchannel = None
    for ch in server.channels:
        if ch.name == "bot-chat" or ch.name == "bot_chat" or ch.name == "bot-commands" or ch.name == "bot_commands":
            botchannel = ch

    if botchannel == None:
        try:
            await client.delete_message(message)
            embed = discord.Embed(
                description="There is not bot commands channel. Please make a channel with one of these names\n\nbot-chat\nbot_chat\nbot-commands\nbot_commands",
                color=0xFF0000
            )
            message = await client.say(embed=embed)
            await asyncio.sleep(3)
            await client.delete_message(message)
        except discord.Forbidden:
            embed = discord.Embed(
                description="Missing permissions",
                color=0xFF0000
            )

            await client.say(embed=embed)
        return False
    else:
        if channel.id == botchannel.id:
            return True
        else:
            try:
                await client.delete_message(message)
                embed = discord.Embed(
                    description="That command can only be used in {}".format(botchannel.mention),
                    color=0xFF0000
                )
                message = await client.say(embed=embed)
                await asyncio.sleep(3)
                await client.delete_message(message)
            except discord.Forbidden:
                embed = discord.Embed(
                    description="Missing permissions",
                    color=0xFF0000
                )

                await client.say(embed=embed)
            return False


@client.command(pass_context=True)
async def cmds(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    if await isBotChannel(ctx.message, channel) == True:
        embed = discord.Embed(
            title="Commands",
            color=0x0000FF
        )
        embed.add_field(name="getkey", value="Get your key", inline=False)
        embed.add_field(name="getroles", value="Get your roles", inline=False)
        embed.add_field(name="getscript", value="Get the script", inline=False)
        embed.add_field(name="botinfo", value="Shows the bot info", inline=False)

        if "457518915061284865" in [y.id for y in author.roles]:
            embed.add_field(name="getkey user",value="Get users key", inline=False)
            embed.add_field(name="getkeyid id", value="Get id's key", inline=False)
            embed.add_field(name="whitelist user true/false",value="Whitelists user premium(true/false)", inline=False)
            embed.add_field(name="remove user",value="Remove users key", inline=False)
            embed.add_field(name="removeid id", value="Remove the user with the id's key", inline=False)
            embed.add_field(name="removekey key",value="Remove the key", inline=False)
            embed.add_field(name="premium user true/false",value="Set users premium to true/false", inline=False)
            embed.add_field(name="blacklist user true/false",value="Set users blacklist to true/false", inline=False)
            embed.add_field(name="blacklistid id", value="Set the user with the id's blacklist to true/false", inline=False)
            embed.add_field(name='info user', value="Get users info", inline=False)

        await client.say(embed=embed)


@client.command(pass_context=True)
async def getkey(ctx, user: discord.Member = None):
    channel = ctx.message.channel
    author = ctx.message.author
    if user == None:
        if await isBotChannel(ctx.message, channel) == True:
            fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=getkey".format(author.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="{}".format(newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                try:
                    embed = discord.Embed(
                        title="Your key",
                        description=message,
                        color=0x00FF00
                    )

                    await client.send_message(author, embed=embed)

                    embed = discord.Embed(
                        description="I have sent you a direct message with your key",
                        color=0x00FF00
                    )

                    await client.say(embed=embed)
                except discord.HTTPException:
                    embed = discord.Embed(
                        description="I can't send any direct messages to you",
                        color=0xFF0000
                    )

                    await client.say(embed=embed)
    else:
        if "Ro-X Development Team" in [y.name for y in author.roles]:
            if user:
                fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=admingetkey&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
                if "error" in message:
                    newMessage = message.replace("error", "")

                    embed = discord.Embed(
                        description="The user {} {}".format(
                            user.mention, newMessage),
                        color=0xFF0000
                    )

                    await client.say(embed=embed)
                else:
                    if "notadmin" not in message:
                        try:
                            embed = discord.Embed(
                                title="{} Key".format(user),
                                description=message,
                                color=0x00FF00
                            )

                            await client.send_message(author, embed=embed)

                            embed = discord.Embed(
                                title="Admin Command",
                                description="I have sent you a direct message with {}'s key".format(user.mention),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
                        except discord.HTTPException:
                            embed = discord.Embed(
                                description="I can't send any direct messages to you",
                                color=0xFF0000
                            )

                            await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description="The input text has too few parameters",
                    color=0xFF0000
                )

                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have access to that command",
                color=0xFF0000
            )

            await client.say(embed=embed)


@client.command(pass_context=True)
async def getkeyid(ctx, id=None):
    if id != None:
        author = ctx.message.author
        fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=admingetkey&targetuserid={}".format(author.id, id))
        mybytes = fp.read()
        message = mybytes.decode("utf8")
        fp.close()
        if "error" in message:
            newMessage = message.replace("error", "")

            embed = discord.Embed(
                description="The user with the id **{}** {}".format(id, newMessage),
                color=0xFF0000
            )

            await client.say(embed=embed)
        else:
            if "notadmin" not in message:
                try:
                    embed = discord.Embed(
                        title="{} Key".format(id),
                        description=message,
                        color=0x00FF00
                    )

                    await client.send_message(author, embed=embed)

                    embed = discord.Embed(
                        title="Admin Command",
                        description="I have sent you a direct message with {}'s key".format(id),
                        color=0x00FF00
                    )

                    await client.say(embed=embed)
                except discord.HTTPException:
                    embed = discord.Embed(
                        description="I can't send any direct messages to you",
                        color=0xFF0000
                    )

                    await client.say(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="The input text has too few parameters",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def getroles(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    server = author.server
    if await isBotChannel(ctx.message, channel) == True:
        fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=getroles".format(author.id))
        mybytes = fp.read()
        message = mybytes.decode("utf8")
        fp.close()
        if "error" in message:
            newMessage = message.replace("error", "")

            embed = discord.Embed(
                description="{}".format(newMessage),
                color=0xFF0000
            )

            await client.say(embed=embed)
        else:
            try:
                if "," in message:
                    roles = message.split(",")
                    roles_to_give = []

                    for role in roles:
                        if role == "Special":
                            if "Special" not in [y.name for y in author.roles]:
                                for role in server.roles:
                                    if str(role) == "Special":
                                        roles_to_give.append(role)
                        elif role == "Premium":
                            if "Ro-X Premium" not in [y.name for y in author.roles]:
                                for role in server.roles:
                                    if str(role) == "Ro-X Premium":
                                        roles_to_give.append(role)
                else:
                    if message == "Special":
                        if "Special" not in [y.name for y in author.roles]:
                            for role in server.roles:
                                if str(role) == "Special":
                                    roles_to_give.append(role)
                    else:
                        if "Member" not in [y.name for y in author.roles]:
                            for role in server.roles:
                                if str(role) == "Member":
                                    roles_to_give.append(role)

                await client.replace_roles(author, *roles_to_give)

                embed = discord.Embed(
                    description="You have been given your roles",
                    color=0x00FF00
                )

                await client.say(embed=embed)
            except discord.Forbidden:
                embed = discord.Embed(
                    description="Missing permissions",
                    color=0xFF0000
                )

                await client.say(embed=embed)

@client.command(pass_context=True)
async def getscript(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    if await isBotChannel(ctx.message, channel) == True:
        if "Special" in [y.name for y in author.roles]:
            try:
                await client.send_file(author, "Project_Ro-X.lua")
                embed = discord.Embed(
                    description="I've sent you the script in a direct message",
                    color=0x00FF00
                )
                await client.say(embed=embed)
            except discord.HTTPException:
                embed = discord.Embed(
                    description="I can't send any direct messages to you",
                    color=0xFF0000
                )

                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have access to that command",
                color=0xFF0000
            )

            await client.say(embed=embed)


@client.command(pass_context=True)
async def whitelist(ctx, user: discord.Member = None, premium: str = None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None and premium != None:
            key = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(50))

            fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=whitelist&targetuserid={}&key={}&premium={}".format(author.id, user.id, key, premium))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    try:
                        roles_to_give = []
                        for role in server.roles:
                            if premium == "true":
                                if role.name == "Special" or role.name == "Ro-X Premium":
                                    roles_to_give.append(role)
                            else:
                                if role.name == "Special":
                                    roles_to_give.append(role)

                        await client.replace_roles(user, *roles_to_give)

                        embed = discord.Embed(
                            description="You have been whitelisted on Project Ro-X\nYour key is: `{}`\nIf you lose the script you can always use the command .getscript to get the script\nHere is the script".format(key),
                            color=0x00FF00
                        )

                        await client.send_message(user, embed=embed)
                        await client.send_file(user, "Project_Ro-X.lua")

                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(user.mention, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    except (discord.Forbidden, discord.HTTPException):
                        embed = discord.Embed(
                            description="Either i'm missing some permissions or i can't send any direct messages to {}".format(user.mention),
                            color=0xFF0000
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters!",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def remove(ctx, user: discord.Member = None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None:
            fp = urllib.request.urlopen(
                "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=remove&targetuserid={}".format(author.id, user.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    try:
                        roles_to_give = []
                        for role in server.roles:
                            if role.name == "Member":
                                roles_to_give.append(role)

                        await client.replace_roles(user, roles_to_give)

                        embed = discord.Embed(
                            description="Your key has been removed on Project Ro-X\nIf you think this is a mistake contact {}".format(
                                server.get_member(457516809940107264).mention),
                            color=0x00FF00
                        )

                        await client.send_message(user, embed=embed)

                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(user.mention, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    except (discord.Forbidden, discord.HTTPException):
                        embed = discord.Embed(
                            description="Either i'm missing some permissions or i can't send any direct messages to {}".format(user.mention),
                            color=0xFF0000
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def removeid(ctx, id=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if id != None:
            fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=remove&targetuserid={}".format(author.id, id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user with the id {} {}".format(
                        id, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                user: discord.Member = None
                for member in server.members:
                    if member.id == user:
                        user = member

                if "notadmin" not in message:
                    if user == None:
                        embed = discord.Embed(
                            title="Admin Command",
                            description="The user with the id {} {}".format(
                                id, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    else:
                        try:
                            roles_to_give = []
                            for role in server.roles:
                                if role.name == "Member":
                                    roles_to_give.append(role)

                            await client.replace_roles(user, roles_to_give)

                            embed = discord.Embed(
                                description="Your key has been removed on Project Ro-X\nIf you think this is a mistake contact {}".format(
                                    server.get_member(457516809940107264).mention),
                                color=0x00FF00
                            )

                            await client.send_message(user, embed=embed)

                            embed = discord.Embed(
                                title="Admin Command",
                                description="The user {} {}".format(
                                    user.mention, message),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
                        except (discord.Forbidden, discord.HTTPException):
                            embed = discord.Embed(
                                description="Either i'm missing some permissions or i can't send any direct messages to {}".format(user.mention),
                                color=0xFF0000
                            )

                            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def removekey(ctx, key=None):
    author = ctx.message.author
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if key != None:
            fp = urllib.request.urlopen(
                "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=removekey&targetkey={}".format(author.id, key))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The key {} {}".format(id, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    embed = discord.Embed(
                        title="Admin Command",
                        description="The key {} {}".format(id, message),
                        color=0x00FF00
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def premium(ctx, user: discord.Member = None, status=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None and status != None:
            message = None
            if status == "true":
                fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=givepremium&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen("https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=removepremium&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    try:
                        if status == "true":
                            if "Ro-X Premium" not in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Ro-X Premium":
                                        await client.add_roles(user, role)
                        else:
                            if "Ro-X Premium" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Ro-X Premium":
                                        await client.remove_roles(user, role)

                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(user.mention, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    except discord.Forbidden:
                        embed = discord.Embed(
                            description="Missing permissions",
                            color=0xFF0000
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def blacklist(ctx, user: discord.Member = None, status=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None and status != None:
            message = None
            if status == "true":
                fp = urllib.request.urlopen(
                    "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=blacklist&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen(
                    "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=unblacklist&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    newMessage = None
                    if status == "true":
                        try:
                            roles_to_give = []
                            for role in server.roles:
                                if role.name == "Muted" or role.name == "Blacklisted":
                                    roles_to_give.append(role)

                            await client.replace_roles(user, *roles_to_give)
                        except discord.Forbidden:
                            embed = discord.Embed(
                                description="Missing permissions",
                                color=0xFF0000
                            )

                            await client.say(embed=embed)
                    else:
                        try:
                            roles_to_give = []
                            for role in server.roles:
                                if role.name == "Special":
                                    roles_to_give.append(role)
                                elif role.name == "Ro-X Premium":
                                    if "premium" in message:
                                        newMessage = message.replace("premium", "")
                                        roles_to_give.append(role)

                            client.replace_roles(user, *roles_to_give)
                        except discord.Forbidden:
                            embed = discord.Embed(
                                description="Missing permissions",
                                color=0xFF0000
                            )

                            await client.say(embed=embed)
                    if newMessage == None:
                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(user.mention, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(
                                user.mention, newMessage),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def blacklistid(ctx, id=None, status=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if id != None and status != None:
            message = None
            if status == "true":
                fp = urllib.request.urlopen(
                    "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=blacklist&targetuserid={}".format(author.id, id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen(
                    "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=unblacklist&targetuserid={}".format(author.id, id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user with the id {} {}".format(
                        id, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    user: discord.Member = None
                    for member in server.members:
                        if member.id == id:
                            user = member

                    newMessage = None
                    if user == None:
                        embed = discord.Embed(
                            description="The user with the id {} {}".format(
                                user.mention, message),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    else:
                        if status == "true":
                            try:
                                roles_to_give = []
                                for role in server.roles:
                                    if role.name == "Muted" or role.name == "Blacklisted":
                                        roles_to_give.append(role)

                                await client.replace_roles(user, *roles_to_give)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description="Missing permissions",
                                    color=0xFF0000
                                )

                                await client.say(embed=embed)
                        else:
                            try:
                                roles_to_give = []
                                for role in server.roles:
                                    if role.name == "Special":
                                        roles_to_give.append(role)
                                    elif role.name == "Ro-X Premium":
                                        if "premium" in message:
                                            newMessage = message.replace("premium", "")
                                            roles_to_give.append(role)

                                client.replace_roles(user, *roles_to_give)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description="Missing permissions",
                                    color=0xFF0000
                                )

                                await client.say(embed=embed)

                    if newMessage == None:
                        if user == None:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="The user with the id {} {}".format(id, message),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="{} {}".format(user.mention, message),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
                    else:
                        if user == None:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="The user with the id {} {}".format(
                                    id, newMessage),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="{} {}".format(
                                    user.mention, newMessage),
                                color=0x00FF00
                            )

                            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    author = ctx.message.author
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None:
            fp = urllib.request.urlopen(
                "https://woodyproducts.casp9536.aspitcloud.dk/projectroxadmin.php?userid={}&action=getinfo&targetuserid={}".format(author.id, user.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=0xFF0000
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    try:
                        ids = message.split(",")

                        embed = discord.Embed(
                            title="{} | User info".format(user),
                            color=0x00FF00
                        )
                        embed.add_field(name="Original User",value="{}".format(ids[0]))
                        embed.add_field(name="Last User",value="{}".format(ids[1]))

                        await client.send_message(author, embed=embed)

                        embed = discord.Embed(
                            description="I have sent you a direct message with {}'s info".format(
                                user.mention),
                            color=0x00FF00
                        )

                        await client.say(embed=embed)
                    except discord.HTTPException:
                        embed = discord.Embed(
                            description="I can't send any direct messages to you",
                            color=0xFF0000
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=0xFF0000
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=0xFF0000
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def botinfo(ctx):
    if await isBotChannel(ctx.message, ctx.message.channel) == True:
        embed = discord.Embed(
            title="",
            description="",
            color=0x0000FF
        )
        embed.set_footer(text="Coded in Python - Project Ro-X Bot")
        embed.set_image(url="httpss://cdn.discordapp.com/avatars/463762798703280128/8617488288a581842d016a3eda0e41c9.png?size=128")
        embed.set_author(name="Bot Information",icon_url="httpss://i.gyazo.com/3484baf8ba09ae77cc6f7e06bbd2eacb.jpg")
        embed.add_field(name="Bot Name", value="Project Ro-X", inline=False)
        embed.add_field(name="Creator", value="Woody#3599", inline=False)
        embed.add_field(name="Version", value="0.5", inline=False)
        embed.add_field(name="Python Version", value=sys.version, inline=False)

        await client.say(embed=embed)

if __name__ == "__main__":
    for extension in extensions:
        try:
            client.load_extension(extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    client.run(TOKEN)
