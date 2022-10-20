#!/usr/bin/env python3

from twitchio.ext import commands
import json

class Bot(commands.Bot):

    def __init__(self):
        # Initialise our Bot with our access token, prefix and a list of channels to join on boot...
        with open('files/secrets.json', 'r') as filp:
            secrets = json.load(filp)
            super().__init__(token=secrets['oauth'], prefix=secrets['prefix'], initial_channels=secrets['channels'])

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f'Logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Send a hello back!
        await ctx.send(f'Hello {ctx.author.name}!')

    @commands.command()
    async def ping(self, ctx: commands.Context):
        # Ping pong
        await ctx.send(f'Pong')
    
    @commands.command()
    async def shoutout(self, ctx: commands.Context):
        if ' ' in ctx.message.content:
            message = ctx.message.content.split(' ')
            await ctx.send(f'Shoutout to {message[1]}! Check them out at https://twitch.tv/{message[1]}')
        else:
            await ctx.send(f'{ctx.author.name}: Provide a username')

    @commands.command()
    async def pronouns(self, ctx: commands.Context):
        await ctx.send(f'My pronouns are she/her')
    
    @commands.command()
    async def lurk(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.name} is now in lurk mode')

    @commands.command()
    async def unlurk(self, ctx: commands.Context):
        await ctx.send(f'{ctx.author.name} has left lurk mode.')

    @commands.command()
    async def donate(self, ctx: commands.Context):
        await ctx.send(f'You can donate here: https://streamelements.com/majoryoshi')
    
    @commands.command()
    async def github(self, ctx: commands.Context):
        await ctx.send(f'Check out my open source projects at https://github.com/TotallyMonica')
    
    @commands.command()
    async def multitwitch(self, ctx: commands.Context):
        streamer = "tygrbyt3"
        await ctx.send(f'Tonight, MajorYoshi is streaming with {streamer}! Watch the both of us here at https://multitwitch.tv/majoryoshi/{streamer}')

    @commands.command()
    async def twitter(self, ctx: commands.Context):
        await ctx.send(f'My twitter is https://twitter.com/yoshithemajor')

    @commands.command()
    async def youtube(self, ctx: commands.Context):
        await ctx.send(f'My YouTube channel is MajorYoshi! Check it out at https://youtube.com/yoshithemajor')

    # @commands.command()
    # async def project(self, ctx: commands.Context):
    #     await ctx.send(f'The project I\'m currenly working on is called Twitch Admin. You can check it out at https://github.com/TotallyMonica/twitch-admin')

bot = Bot()
bot.run()