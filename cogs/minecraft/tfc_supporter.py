import discord
from discord import app_commands
from discord.ext import commands
from util.glovalvar import myguild
from collections import deque


allowed_numbers = [16, 13, 7, 2, -3, -6, -9, -15]
def min_combinations(target: int, required_sequence: list[int]) -> list[int] | None:
    required_sum = sum(required_sequence)
    adjusted_target = target - required_sum

    if adjusted_target == 0:
        return required_sequence

    queue = deque([(0, [])])
    visited = set([0])

    while queue:
        current_sum, path = queue.popleft()

        for number in allowed_numbers:
            new_sum = current_sum + number

            if new_sum == adjusted_target:
                return path + [number] + required_sequence

            if new_sum not in visited and new_sum <= adjusted_target:
                visited.add(new_sum)
                queue.append((new_sum, path + [number]))

    return None


class tfg_supporter(commands.Cog):
    @app_commands.guild_only()
    @app_commands.guilds(myguild)
    @app_commands.command(name="tfc_hammer_calc")
    async def hammer_calc(self, ctx: discord.Interaction, target: int, required_sequence: str):
        try:
            required_sequence = list(map(int, required_sequence.split()))
        except Exception:
            await ctx.response.send_message("要求シーケンスが間違っている可能性があります。")
            return
        res = min_combinations(target, required_sequence)
        messages = [
            f"Target: {target}",
            f"Required Sequence: {required_sequence}",
            "Output: " + (", ".join(list(map(str, res))) if res is not None else "None")
        ]
        await ctx.response.send_message("\n".join(messages))


async def setup(bot):
    await bot.add_cog(tfg_supporter(bot))
