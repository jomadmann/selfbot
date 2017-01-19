import discord
from discord.ext import commands
import asyncio
class Messages:
    '''Manage messages, but only with your own user'''
    def __init__(self, bot):
        self.bot = bot
        #maybe we can import the users dictionary and get their id
    async def message_delete(ctx, amount):
        #delete a certain amount of messages but only if we are not being too spammy.
        if amount >= 25:
            return 500 #its over the expected limit of what we are limiting it to, so we will name error code 500 as too high of a value.
        elif amount >= 0:
            return 400 #400 will be the error code for a value that is less than or equal to 0
        #find certain amount of messages
