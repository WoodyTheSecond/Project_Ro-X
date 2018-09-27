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
        await client.delete_message(message)
        embed = discord.Embed(
            description="There is not bot commands channel. Please make a channel with one of these names\n\nbot-chat\nbot_chat\nbot-commands\nbot_commands",
            color=discord.Color.red()
        )
        message = await client.say(embed=embed)
        await asyncio.sleep(3)
        await client.delete_message(message)
        return False
    else:
        if channel.id == botchannel.id:
            return True
        else:
            await client.delete_message(message)
            embed = discord.Embed(
                description="That command can only be used in {}".format(
                    botchannel.mention),
                color=discord.Color.red()
            )
            message = await client.say(embed=embed)
            await asyncio.sleep(3)
            await client.delete_message(message)
            return False


@client.command(pass_context=True)
async def cmds(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    if await isBotChannel(ctx.message, channel) == True:
        embed = discord.Embed(
            title="Commands",
            description="",
            color=discord.Color.blue()
        )
        embed.add_field(name="getkey", value="Get your key", inline=False)
        embed.add_field(name="getroles", value="Get your roles", inline=False)
        embed.add_field(name="getscript", value="Get the script", inline=False)
        embed.add_field(
            name="botinfo", value="Shows the bot info", inline=False)

        if "457518915061284865" in [y.id for y in author.roles]:
            embed.add_field(name="getkey @user",
                            value="Get users key", inline=False)
            embed.add_field(name="whitelist @user true/false",
                            value="Whitelists user premium(true/false)", inline=False)
            embed.add_field(name="remove @user",
                            value="Remove users key", inline=False)
            embed.add_field(
                name="removeid id", value="Remove the user with the id's key", inline=False)
            embed.add_field(name="removekey key",
                            value="Remove the key", inline=False)
            embed.add_field(name="premium @user true/false",
                            value="Set users premium to true/false", inline=False)
            embed.add_field(name="blacklist @user true/false",
                            value="Set users blacklist to true/false", inline=False)
            embed.add_field(
                name="blacklistid id", value="Set the user with the id's blacklist to true/false", inline=False)
            embed.add_field(name='info @user',
                            value="Get users info", inline=False)

        await client.say(embed=embed)


@client.command(pass_context=True)
async def getkey(ctx, user: discord.Member = None):
    channel = ctx.message.channel
    author = ctx.message.author
    if user == None:
        if await isBotChannel(ctx.message, channel) == True:
            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=getkey".format(author.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="{}".format(newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    title="Your key",
                    description=message,
                    color=discord.Color.green()
                )

                await client.send_message(author, embed=embed)

                embed = discord.Embed(
                    description="I have sent you a direct message with your key",
                    color=discord.Color.green()
                )

                await client.say(embed=embed)
    else:
        if "Ro-X Development Team" in [y.name for y in author.roles]:
            if user:
                fp = urllib.request.urlopen(
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=admingetkey&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
                if "error" in message:
                    newMessage = message.replace("error", "")

                    embed = discord.Embed(
                        description="The user {} {}".format(
                            user.mention, newMessage),
                        color=discord.Color.red()
                    )

                    await client.say(embed=embed)
                else:
                    if "notadmin" not in message:
                        embed = discord.Embed(
                            title="{} Key".format(user),
                            description=message,
                            color=discord.Color.green()
                        )

                        await client.send_message(author, embed=embed)

                        embed = discord.Embed(
                            title="Admin Command",
                            description="I have sent you a direct message with {}'s key".format(
                                user.mention),
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description="The input text has too few parameters",
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have access to that command",
                color=discord.Color.red()
            )

            await client.say(embed=embed)


@client.command(pass_context=True)
async def getkeyid(ctx, id=None):
    if id != None:
        author = ctx.message.author
        fp = urllib.request.urlopen("http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=admingetkey&targetuserid={}".format(author.id, id))
        mybytes = fp.read()
        message = mybytes.decode("utf8")
        fp.close()
        if "error" in message:
            newMessage = message.replace("error", "")

            embed = discord.Embed(
                description="The user with the id **{}** {}".format(id, newMessage),
                color=discord.Color.red()
            )

            await client.say(embed=embed)
        else:
            if "notadmin" not in message:
                embed = discord.Embed(
                    title="{} Key".format(id),
                    description=message,
                    color=discord.Color.green()
                )

                await client.send_message(author, embed=embed)

                embed = discord.Embed(
                    title="Admin Command",
                    description="I have sent you a direct message with {}'s key".format(id),
                    color=discord.Color.green()
                )

                await client.say(embed=embed)
    else:
        embed = discord.Embed(
            title="Error",
            description="The input text has too few parameters",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def getroles(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    server = author.server
    if await isBotChannel(ctx.message, channel) == True:
        fp = urllib.request.urlopen(
            "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=getroles".format(author.id))
        mybytes = fp.read()
        message = mybytes.decode("utf8")
        fp.close()
        if "error" in message:
            newMessage = message.replace("error", "")

            embed = discord.Embed(
                description="{}".format(newMessage),
                color=discord.Color.red()
            )

            await client.say(embed=embed)
        else:
            if "," in message:
                roles = message.split(",")

                for role in roles:
                    if role == "Special":
                        if "Special" not in [y.name for y in author.roles]:
                            for role in server.roles:
                                if str(role) == "Special":
                                    await client.add_roles(author, role)
                    elif role == "Premium":
                        if "Ro-X Premium" not in [y.name for y in author.roles]:
                            for role in server.roles:
                                if str(role) == "Ro-X Premium":
                                    await client.add_roles(author, role)
            else:
                if message == "Special":
                    if "Special" not in [y.name for y in author.roles]:
                        for role in server.roles:
                            if str(role) == "Special":
                                await client.add_roles(author, role)
                else:
                    if "Member" not in [y.name for y in author.roles]:
                        for role in server.roles:
                            if str(role) == "Member":
                                await client.add_roles(author, role)

            embed = discord.Embed(
                description="You have been gives your roles",
                color=discord.Color.green()
            )

            await client.say(embed=embed)


@client.command(pass_context=True)
async def getscript(ctx):
    channel = ctx.message.channel
    author = ctx.message.author
    if await isBotChannel(ctx.message, channel) == True:
        if "Special" in [y.name for y in author.roles]:
            await client.send_file(author, "Project_Ro-X.lua")
            embed = discord.Embed(
                description="I've sent you the script in a direct message",
                color=discord.Color.green()
            )
            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                description="You don't have access to that command",
                color=discord.Color.red()
            )

            await client.say(embed=embed)


@client.command(pass_context=True)
async def whitelist(ctx, user: discord.Member = None, premium=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None and premium != None:
            key = "".join(random.choice(string.ascii_lowercase +
                                        string.ascii_uppercase + string.digits) for _ in range(50))

            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=whitelist&targetuserid={}&key={}&premium={}".format(author.id, user.id, key, premium))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    if "Member" in [y.name for y in user.roles]:
                        for role in server.roles:
                            if str(role) == "Member":
                                await client.remove_roles(user, role)
                    if "Special" not in [y.name for y in user.roles]:
                        for role in server.roles:
                            if str(role) == "Special":
                                await client.add_roles(user, role)
                    if premium == "true":
                        if "Ro-X Premium" not in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Ro-X Premium":
                                    await client.add_roles(user, role)

                    embed = discord.Embed(
                        description="You have been whitelisted on Project Ro-X\nYour key is: `{}`\nIf you lose the script you can always use the command .getscript to get the script\nHere is the script".format(
                            key),
                        color=discord.Color.green()
                    )

                    await client.send_message(user, embed=embed)
                    await client.send_file(user, "Project_Ro-X.lua")

                    embed = discord.Embed(
                        title="Admin Command",
                        description="{} {}".format(user.mention, message),
                        color=discord.Color.green()
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters!",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def remove(ctx, user: discord.Member = None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None:
            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=remove&targetuserid={}".format(author.id, user.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    if "Member" not in [y.name for y in user.roles]:
                        for role in server.roles:
                            if str(role) == "Member":
                                await client.add_roles(user, role)
                    if "Special" in [y.name for y in user.roles]:
                        for role in server.roles:
                            if str(role) == "Special":
                                await client.remove_roles(user, role)
                    if "Ro-X Premium" in [y.name for y in user.roles]:
                        for role in server.roles:
                            if str(role) == "Ro-X Premium":
                                await client.remove_roles(user, role)

                    embed = discord.Embed(
                        description="Your key has been removed on Project Ro-X\nIf you think this is a mistake contact {}".format(
                            server.get_member(457516809940107264).mention),
                        color=discord.Color.green()
                    )

                    await client.send_message(user, embed=embed)

                    embed = discord.Embed(
                        title="Admin Command",
                        description="{} {}".format(user.mention, message),
                        color=discord.Color.green()
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def removeid(ctx, id=None):
    author = ctx.message.author
    server = author.server
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if id != None:
            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=remove&targetuserid={}".format(author.id, id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user with the id {} {}".format(
                        id, newMessage),
                    color=discord.Color.red()
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
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
                    else:
                        if "Member" not in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Member":
                                    await client.add_roles(user, role)
                        if "Special" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Special":
                                    await client.remove_roles(user, role)
                        if "Ro-X Premium" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Ro-X Premium":
                                    await client.remove_roles(user, role)

                        embed = discord.Embed(
                            description="Your key has been removed on Project Ro-X\nIf you think this is a mistake contact {}".format(
                                server.get_member(457516809940107264).mention),
                            color=discord.Color.green()
                        )

                        await client.send_message(user, embed=embed)

                        embed = discord.Embed(
                            title="Admin Command",
                            description="The user {} {}".format(
                                user.mention, message),
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def removekey(ctx, key=None):
    author = ctx.message.author
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if key != None:
            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=removekey&targetkey={}".format(author.id, key))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()
            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The key {} {}".format(id, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    embed = discord.Embed(
                        title="Admin Command",
                        description="The key {} {}".format(id, message),
                        color=discord.Color.green()
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
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
                fp = urllib.request.urlopen(
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=givepremium&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen(
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=removepremium&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
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
                        color=discord.Color.green()
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
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
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=blacklist&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen(
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=unblacklist&targetuserid={}".format(author.id, user.id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    newMessage = None
                    if status == "true":
                        if "Member" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Member":
                                    await client.remove_roles(user, role)
                        if "Special" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Special":
                                    await client.remove_roles(user, role)
                        if "Ro-X Premium" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Ro-X Premium":
                                    await client.remove_roles(user, role)
                        if "Muted" not in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Muted":
                                    await client.add_roles(user, role)
                        if "Blacklisted" not in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Blacklisted":
                                    await client.add_roles(user, role)
                    else:
                        if "Member" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Member":
                                    await client.remove_roles(user, role)
                        if "Special" not in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Special":
                                    await client.add_roles(user, role)
                        if "premium" in message:
                            newMessage = message.replace("premium", "")
                            if "Ro-X Premium" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Ro-X Premium":
                                        await client.remove_roles(user, role)
                        if "Muted" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Muted":
                                    await client.remove_roles(user, role)
                        if "Blacklisted" in [y.name for y in user.roles]:
                            for role in server.roles:
                                if str(role) == "Blacklisted":
                                    await client.remove_roles(user, role)

                    if newMessage == None:
                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(user.mention, message),
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Admin Command",
                            description="{} {}".format(
                                user.mention, newMessage),
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
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
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=blacklist&targetuserid={}".format(author.id, id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()
            else:
                fp = urllib.request.urlopen(
                    "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=unblacklist&targetuserid={}".format(author.id, id))
                mybytes = fp.read()
                message = mybytes.decode("utf8")
                fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user with the id {} {}".format(
                        id, newMessage),
                    color=discord.Color.red()
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
                            color=discord.Color.green()
                        )

                        await client.say(embed=embed)
                    else:
                        if status == "true":
                            if "Member" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Member":
                                        await client.remove_roles(user, role)
                            if "Special" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Special":
                                        await client.remove_roles(user, role)
                            if "Ro-X Premium" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Ro-X Premium":
                                        await client.remove_roles(user, role)
                            if "Muted" not in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Muted":
                                        await client.add_roles(user, role)
                            if "Blacklisted" not in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Blacklisted":
                                        await client.add_roles(user, role)
                        else:
                            if "Member" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Member":
                                        await client.remove_roles(user, role)
                            if "Special" not in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Special":
                                        await client.add_roles(user, role)
                            if "premium" in message:
                                newMessage = message.replace("premium", "")
                                if "Ro-X Premium" in [y.name for y in user.roles]:
                                    for role in server.roles:
                                        if str(role) == "Ro-X Premium":
                                            await client.remove_roles(user, role)
                            if "Muted" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Muted":
                                        await client.remove_roles(user, role)
                            if "Blacklisted" in [y.name for y in user.roles]:
                                for role in server.roles:
                                    if str(role) == "Blacklisted":
                                        await client.remove_roles(user, role)

                    if newMessage == None:
                        if user == None:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="The user with the id {} {}".format(
                                    id, message),
                                color=discord.Color.green()
                            )

                            await client.say(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="{} {}".format(
                                    user.mention, message),
                                color=discord.Color.green()
                            )

                            await client.say(embed=embed)
                    else:
                        if user == None:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="The user with the id {} {}".format(
                                    id, newMessage),
                                color=discord.Color.green()
                            )

                            await client.say(embed=embed)
                        else:
                            embed = discord.Embed(
                                title="Admin Command",
                                description="{} {}".format(
                                    user.mention, newMessage),
                                color=discord.Color.green()
                            )

                            await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def info(ctx, user: discord.Member = None):
    author = ctx.message.author
    if "Ro-X Development Team" in [y.name for y in author.roles]:
        if user != None:
            fp = urllib.request.urlopen(
                "http://woodyproducts.000webhostapp.com/projectroxadmin.php?userid={}&action=getinfo&targetuserid={}".format(author.id, user.id))
            mybytes = fp.read()
            message = mybytes.decode("utf8")
            fp.close()

            if "error" in message:
                newMessage = message.replace("error", "")

                embed = discord.Embed(
                    description="The user {} {}".format(
                        user.mention, newMessage),
                    color=discord.Color.red()
                )

                await client.say(embed=embed)
            else:
                if "notadmin" not in message:
                    ids = message.split(",")

                    embed = discord.Embed(
                        title="{} | User info".format(user),
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Original User",
                                    value="{}".format(ids[0]))
                    embed.add_field(name="Last User",
                                    value="{}".format(ids[1]))

                    await client.send_message(author, embed=embed)

                    embed = discord.Embed(
                        description="I have sent you a direct message with {}'s info".format(
                            user.mention),
                        color=discord.Color.green()
                    )

                    await client.say(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="The input text has too few parameters",
                color=discord.Color.red()
            )

            await client.say(embed=embed)
    else:
        embed = discord.Embed(
            description="You don't have access to that command",
            color=discord.Color.red()
        )

        await client.say(embed=embed)


@client.command(pass_context=True)
async def botinfo(ctx):
    if isBotChannel(ctx.message, ctx.message.channel) == True:
        embed = discord.Embed(
            title="",
            description="",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Coded in Python - Project Ro-X Bot")
        embed.set_image(
            url="https://cdn.discordapp.com/avatars/463762798703280128/8617488288a581842d016a3eda0e41c9.png?size=128")
        embed.set_author(name="Bot Information",
                         icon_url="https://i.gyazo.com/3484baf8ba09ae77cc6f7e06bbd2eacb.jpg")
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
