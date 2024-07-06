import discord
from discord import app_commands
from discord.ext import commands
from util.glovalvar import myguild

tier_list = [
    'ULV',
    'LV',
    'MV',
    'HV',
    'EV',
    'IV',
    'LuV',
    'ZPM',
    'UV',
    'UHV',
    'UEV',
    'UIV',
    'UXV',
    'OpV',
    'MAX'
]


class gt_voltage(commands.Cog):
    @app_commands.guild_only()
    @app_commands.guilds(myguild)
    @app_commands.command(name="gt_voltage")
    async def gt_voltage(self, ctx: discord.Interaction, voltage: int, time: float):
        embed = discord.Embed(title='', description=f'Total Energy: __{voltage*int(time*20)} EU__', color=0x00ffff)
        tiers = 0
        tier_list_num = 0
        tier_energy = 8

        while 0 < int(20*(time/(2**tiers)))/20 and tier_list_num < 15:

            if voltage <= tier_energy:
                tier = tier_list[tier_list_num]
                embed.add_field(name=f'{tier} ({voltage*(4**tiers)} EU/t)', value=f'{int(20*(time/(2**tiers)))/20}s ({(int(20*(time/(2**tiers))))}t)', inline=False)
                tiers += 1
                tier_energy *= 4
                tier_list_num += 1
            else:
                if voltage > 2147483648:
                    tier = 'MAX'
                    embed.add_field(name=f'{tier} ({voltage*(4**tiers)} EU/t)', value=f'{int(20*(time/(2**tiers)))/20}s ({(int(20*(time/(2**tiers))))}t)', inline=False)

        embed.title = f'Voltage: __{embed.fields[0].name}__, Time: __{time} sec__'
        await ctx.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(gt_voltage(bot))
