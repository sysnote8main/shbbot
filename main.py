import discord
from discord.ext import commands
import os
import datetime
import util.glovalvar
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = os.getenv("DISCORD_GUILD_ID")
myguild = discord.Object(GUILD_ID)
util.glovalvar.myguild = myguild

# import nest_asyncio
# nest_asyncio.apply()

prefix = "!"

cogs: list[str] = [
    "helloworld",
]
ownerId: int = 727491451805761537


def isBotOwner(ctx):
    return ctx.message.author.id == ownerId


class MyBot(commands.Bot):
    async def setup_hook(self) -> None:
        for cog in cogs:
            try:
                await self.load_extension("cogs." + cog)
            except Exception as e:
                print(e)
        await self.tree.sync(guild=myguild)


intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.voice_states = True
intents.dm_messages = True
bot: commands.Bot = MyBot(command_prefix=prefix, intents=intents)


def getCogName(name: str) -> str:
    return "cogs." + name


@bot.event
async def on_ready():
    print("Bot on ready with " + bot.user.display_name)


@bot.event
async def on_command_error(ctx: commands.Context, error):
    if ctx.author.bot:
        return
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(
            "このコマンドは存在していないか、権限不足のため使用することができません。",
            ephemeral=True,
        )


@bot.command(name="owner/load_ext")
@commands.check(isBotOwner)
async def _load_ext(ctx: commands.Context, name: str):
    #await ctx.message.delete()
    try:
        await bot.load_extension(getCogName(name))
        await ctx.author.send(f"Successfully to load! (ext:{name})")
    except Exception as e:
        await ctx.author.send(f"Failed to load. (ext:{name})\n```{e}```")


@bot.command(name="owner/unload_ext")
@commands.check(isBotOwner)
async def _unload_ext(ctx: commands.Context, name: str):
    #await ctx.message.delete()
    try:
        await bot.unload_extension(getCogName(name))
        await ctx.author.send(f"Successfully to unload! (ext:{name})")
    except Exception as e:
        await ctx.author.send(f"Failed to unload. (ext:{name})\n```{e}```")


@bot.command(name="owner/reload_ext")
@commands.check(isBotOwner)
async def _reload_ext(ctx: commands.Context, name: str):
    #await ctx.message.delete()
    try:
        await bot.unload_extension(getCogName(name))
        await bot.load_extension(getCogName(name))
        await ctx.author.send(f"Successfully to reload! (ext:{name})")
    except Exception as e:
        await ctx.author.send(f"Failed to reload. (ext:{name})\n```{e}```")


@bot.command(name="owner/reload_slash")
@commands.check(isBotOwner)
async def _sync_tree_cmd(ctx: commands.Context):
    dt = datetime.datetime.now()
    print("[Owner-Discord] Reload slash commands")
    #await ctx.message.delete()
    await ctx.reply("Syncing slash commands...")
    msg = ""
    try:
        await bot.tree.sync(guild=myguild)
        msg = "Successfully to sync slash commands!"
    except Exception as e:
        msg = f"Failed to sync slash commands.\n```{e}```"
    dt = datetime.datetime.now() - dt
    msg += f"\n(Execution time: {dt})"
    await ctx.author.send(msg)
    print(f"[Owner-Discord] Finished to reload slash commands (time: {dt})")


if TOKEN == "":
    print("Failed to load token!")
    exit(1)
bot.run(token=TOKEN)
