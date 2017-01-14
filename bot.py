import discord
from discord.ext import commands
import os
import asyncio
import sys
from time import gmtime, strftime
from ext.dataIO import dataIO
bot = commands.Bot(command_prefix="=+", self_bot=True)
ownerid = "put your id here"
awayreason = ""
command__list = ['quote', 'ping', 'commands', 'user', 'server', 'away', 'emoji or em']
userinfo = {}
emojiList = {'worlds':'【=◈︿◈=】', 'wave':'(°▽°)/','hug':'(づ ◕‿◕ )づ','owo':'(＾• ω •＾)','tabledown':'┬─┬ノ( º _ ºノ)	', 'crying':'.｡･ﾟﾟ･(＞_＜)･ﾟﾟ･｡.', 'lenny':'( ͡° ͜ʖ ͡°)', 'oh':'(ᵔ.ᵔ)','doubt':'(←_←)'}
def setup_func():
    data = {"email":"none", "id":"none", "password":"none" }
    print("Type your email")
    email = input("> ")
    if "@" not in email:
        print("That is not a vaild email.")
        os.rmdir("data")
        return
    data["email"] = email
    print("Type your password")
    passwd = input("> ")
    data["password"] = passwd
    print("Input your id")
    ownerid = input("> ")
    data["id"] = ownerid
    dataIO.save_json("data/userinf.json", data)

def __init__():
    if not os.path.exists("data"):
        os.makedirs("data")
        setup_func()
    global userinfo
    userinfo = dataIO.load_json("data/userinf.json")
    ownerid = userinfo["id"]
@bot.command(pass_context=True, hidden=True)
async def debug(ctx, *, code):
    """Evaluates code
        Modified function, originally made by Rapptz"""
    if ctx.message.author.id == userinfo["id"]:
        print("found owner")
        code = code.strip('` ')
        python = '```py\n{}\n```'
        result = None
        global_vars = globals().copy()
        global_vars['bot'] = bot
        global_vars['ctx'] = ctx
        global_vars['message'] = ctx.message
        global_vars['author'] = ctx.message.author
        global_vars['channel'] = ctx.message.channel
        global_vars['server'] = ctx.message.server
        try:
            result = eval(code, global_vars, locals())
        except Exception as e:
            await bot.edit_message(ctx.message, python.format(type(e).__name__ + ': ' + str(e)))
            return
        if asyncio.iscoroutine(result):
            result = await result

            result = python.format(result)

            await bot.edit_message(ctx.message, result)
@bot.command(pass_context=True,name="emoji", aliases=["em"])
async def emoji__command(ctx,*, emoji):
    if emoji in emojiList:
        await bot.edit_message(ctx.message, emojiList[emoji])
@bot.command(pass_context=True,name="emojilist")
async def listemojis(ctx):
    emlist = "Emojis are:\n"
    for emoji in emojiList:
        emlist += "`" + str(emoji) + "`\n"
    em = discord.Embed(title="Emoji List", description=emlist, colour=0x1D84B9)
    em.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    await bot.edit_message(ctx.message,embed=em)

@bot.command(pass_context=True)
async def away(ctx, * ,reason:str=None):
    global awayreason

    global away
    if reason is None:
        awayreason = "AFK"
    else:
        awayreason = reason
    if away:
        away = False
        await bot.edit_message(ctx.message, embed=discord.Embed(title="Update Status",description="Alright, you are no longer away!", colour=0x00FF99))
    else:
        away = True
        await bot.edit_message(ctx.message, embed=discord.Embed(title="Update Status",description="Alright, you are away!", colour=0x00FF99))
@bot.command(pass_context=True)
async def quote(ctx, message_id:str=None):
    if message_id is None:
        em = discord.Embed(title="Error",description="The bot encountered an error; The error is no message id found.", colour=0xFF5959)
        em.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
        # em.set_footer(set the default datetime thing ive been using)
        await bot.edit_message(ctx.message, embed=em)
    else:
        async for message in bot.logs_from(ctx.message.channel, limit=500):
            if message.id == message_id:
                if message is not None:
                    em = discord.Embed(title=message.content, colour=0x33CC66)
                    em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                    em.set_footer(text='Discordian Self-Bot at {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                    await bot.edit_message(ctx.message,embed=em)
                elif message is None:
                    print("Message with id of -{}- was not found".format(message_id))
                    #post the embed error but altered.`
@bot.command(name='server', pass_context=True)
async def _serverinfo(ctx):
    '''Provides info on a server, '''

    if ctx.message.channel.is_private:
        await bot.edit_message(ctx,message, embed = discord.Embed(color = 15746887, description = '**Error**: _Cannot be used in a PM_'))
        return

    server = ctx.message.server
    info_embed = discord.Embed(color = server.owner.color)

    info_embed.set_author(name = server.name,
                          icon_url = server.icon_url)

    info_embed.add_field(name = "Owner", value = "<@!{}>".format(server.owner.id))
    info_embed.add_field(name = "ID", value = server.id)
    info_embed.add_field(name = "Created At", value = str(server.created_at))
    info_embed.add_field(name = "Channels", value = len(server.channels))
    info_embed.add_field(name = "Members", value = server.member_count)
    info_embed.add_field(name = "Roles", value = len(server.roles))
    info_embed.add_field(name = "Region", value = str(server.region))
    info_embed.add_field(name = "AFK Timeout", value = "{} minutes".format(server.afk_timeout/60).replace(".0", ""))
    info_embed.add_field(name = "AFK Channel", value = str(server.afk_channel))
    info_embed.add_field(name = "Verification Level", value = str(server.verification_level))
    if len(str(server.emojis)) < 1024 and server.emojis:
        info_embed.add_field(name = "Emojis", value = " ".join([str(emoji) for emoji in server.emojis]), inline = False)
    elif len(str(server.emojis)) >= 1024:
        info_embed.add_field(name= "Emojis", value = "**Error**: _Too many emojis_", inline = False)

    await bot.edit_message(ctx.message, embed = info_embed)

@bot.command(pass_context=True, name='user')
async def userinfo(ctx, *, user : discord.Member=None):
    '''Provides info on a user'''
    if ctx.message.channel.is_private:
        await bot.edit_message(ctx.message,embed = discord.Embed(color = 15746887, description = "**Error**: May not be used in PM."))
        return
    if user is None:
        user = ctx.message.author
    elif user.bot:
        await bot.edit_message(ctx.message,embed = discord.Embed(color = 15746887, description = "**Error**: Bot accounts do not work at this time"))
        return
    else:
        pass
    info_embed = (discord.Embed(color = 15746887))
    info_embed.set_author(name = user.name, icon_url = user.avatar_url)
    info_embed.add_field(name = "Username", value=user.mention)
    info_embed.add_field(name = "ID", value = user.id)
    info_embed.add_field(name = "Created At", value = str(user.created_at))
    rolelist = ', '.join(role.name for role in user.roles[1:])
    if len(rolelist) >= 500:
        info_embed.add_field(name = "Roles", value = "**Error:***_Too many roles._")
    else:
        info_embed.add_field(name = "Roles", value = rolelist)
    await bot.edit_message(ctx.message,embed = info_embed)

@bot.command(pass_context=True)
async def commands(ctx):
    cmdlist = "Commands are:\n"
    for cmd in command__list:
        cmdlist += "`" + str(cmd) + "`\n"
    em = discord.Embed(title="Command List", description=cmdlist, colour=0x1D84B9)
    em.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    await bot.edit_message(ctx.message,embed=em)
@bot.event
async def on_ready():
    print("--"*5)
    print("Logged in as")
    print(bot.user.id)
    print("client starting...")
    print("--"*5)
@bot.event
async def on_message(message):
    if message.author.id == ownerid:
        await bot.process_commands(message)
    elif away:
        if message.channel.type.name is "private":
            await bot.send_message(message.channel, embed=discord.Embed(title="I'm Away!", description=awayreason, colour=0x1D84B9))
        if bot.user in message.mentions:
            await bot.send_message(message.channel, embed=discord.Embed(title="I'm Away!", description=awayreason, colour=0x1D84B9))
    else:
        return
@bot.command(pass_context=True)
async def ping(ctx):
    msg = discord.Embed(title='Pong!', colour=0x66CC99)
    msg.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    msg.set_footer(text='Discordian Self-Bot at {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    await bot.edit_message(ctx.message,embed=msg)
if not os.path.exists("data"):
    os.makedirs("data")
    setup_func()
userinfo = dataIO.load_json("data/userinf.json")
away = False
ownerid = userinfo["id"]
bot.run(userinfo["email"],userinfo["password"], bot=False)
