"""Generic example of the command pattern used in the bot.

An async slash command that defers (so Discord does not time out), reads
from SQLite, and replies with an embed. Sample only: no production logic.
"""
import os

import aiosqlite
import discord
from discord import app_commands

DB_PATH = os.getenv("DB_PATH", "example.db")


class ExampleBot(discord.Client):
    def __init__(self) -> None:
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        await self.tree.sync()


bot = ExampleBot()


@bot.tree.command(name="record", description="Show the overall prediction record")
async def record(interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)

    async with aiosqlite.connect(DB_PATH) as db:
        query = (
            "SELECT COUNT(*), COALESCE(SUM(result = 'win'), 0) "
            "FROM predictions WHERE result IN ('win', 'loss')"
        )
        async with db.execute(query) as cursor:
            total, wins = await cursor.fetchone()

    hit_rate = (wins / total * 100) if total else 0.0
    embed = discord.Embed(
        title="Prediction record",
        description=f"{wins} of {total} graded predictions ({hit_rate:.1f}%)",
    )
    await interaction.followup.send(embed=embed)


if __name__ == "__main__":
    # The token comes from the environment, never from source code.
    bot.run(os.environ["DISCORD_TOKEN"])
