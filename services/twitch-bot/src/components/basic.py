from twitchio.ext import commands

class Basic(commands.Component):

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")