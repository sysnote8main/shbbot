from discord import app_commands
from discord.ext import commands
from util.glovalvar import myguild
import random


def roll(count: int, face: int):
    return [str(random.randint(1, face)) for i in range(count)]


class dice(commands.Cog):
    @commands.hybrid_command()
    @app_commands.guilds(myguild)
    async def roll(self, ctx: commands.Context):
        await ctx.send(" ".join(roll(1, 100)))


async def setup(bot):
    await bot.add_cog(dice(bot))
