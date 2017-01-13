import discord
from discord.ext import commands
from time import gmtime, strftime
bot = commands.Bot(command_prefix="=+", self_bot=True)
ownerid = bot.user.id
away = False
awayreason = ""
command__list = ['quote', 'ping', 'commands']
@bot.command(pass_context=True)
async def away(toggle, *,reason):
    global away
    if away:
        away = False
    elif away is False:
        away = True
@bot.command(pass_context=True)
async def quote(ctx, message_id:str=None):
    if message_id is None:
        em = discord.Embed(title="Error",description="The bot encountered an error; The error is no message id found.", colour=0xFF5959)
        em.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
        # em.set_footer(set the default datetime thing ive been using)
        await bot.say(embed=em)
    else:
        async for message in bot.logs_from(ctx.message.channel, limit=500):
            if message.id == message_id:
                if message is not None:
                    em = discord.Embed(title=message.content, colour=0x33CC66)
                    em.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
                    em.set_footer(text='Discordian Self-Bot at {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
                    await bot.say(embed=em)
                elif message is None:
                    print("Message with id of -{}- was not found".format(message_id))
                    #post the embed error but altered.`
@bot.command()
async def commands():
    cmdlist = "Commands are:\n"
    for cmd in command__list:
        cmdlist += "`" + str(cmd) + "`\n"
    em = discord.Embed(title="Command List", description=cmdlist, colour=0x1D84B9)
    em.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    await bot.say(embed=em)
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
    else:
        return
@bot.event
async def on_command(command, ctx):
    await bot.delete_message(ctx.message)
@bot.command()
async def ping():
    msg = discord.Embed(title='Pong!', colour=0x66CC99)
    msg.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    msg.set_footer(text='Discordian Self-Bot at {}'.format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    await bot.say(embed=msg)



bot.run('email','password', bot=False)
