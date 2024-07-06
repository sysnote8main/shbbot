import discord
from discord import app_commands
from discord.ext import commands
from util.glovalvar import myguild


class helloworld(commands.Cog):
    @app_commands.guild_only()
    @app_commands.guilds(myguild)
    @app_commands.command(name="hw")
    async def helloworld(self, ctx: discord.Interaction):
        await ctx.response.send_message("Hello world!")


async def setup(bot):
    await bot.add_cog(helloworld(bot))
