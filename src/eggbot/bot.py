from __future__ import annotations

import os

import discord
from discord.ext import commands
from discord.ext.commands import Context
from runtime_yolk import Yolk


# Initialize runtime and bot client
runtime = Yolk()
runtime.set_logging("DEBUG")
runtime.load_env()
logger = runtime.get_logger(__name__)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready() -> None:
    """Simple console logging indicating ready event has fired."""
    logger.info("Eggbot has successfully loaded. In %s as %s", bot.guilds, bot.user.id)


@bot.command()
async def hello(ctx: Context) -> None:
    logger.info("Eggbot hello command recieved. Hello there!")
    if ctx.guild.id != 190604982934831104:
        logger.warning("Listening to the wrong guild! %s", ctx.channel.guild.name)
    await ctx.channel.send(f"Hello to you as well, {ctx.author.mention}!")


@bot.command()
async def shutdown(ctx: Context) -> None:
    logger.info("Eggbot shutdown command recieved.  Until next time, space cowboy.")
    if ctx.guild.id != 190604982934831104:
        logger.warning("Listening to the wrong guild! %s", ctx.channel.guild.name)
    await ctx.channel.send(f"See you next time, {ctx.author.mention}.")
    await bot.close()


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
