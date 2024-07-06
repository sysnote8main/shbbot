from discord import app_commands
from discord.ext import commands
from util.glovalvar import myguild


class dice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    @app_commands.guilds(myguild)
    async def roll(self, ctx: commands.Context):
        await ctx.send(f"Now ping: {round(self.bot.latency*1000)}ms")


async def setup(bot):
    await bot.add_cog(dice(bot))
