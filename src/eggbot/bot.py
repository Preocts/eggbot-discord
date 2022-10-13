from __future__ import annotations

import discord
from discord.ext import commands
from discord.ext.commands import CommandError
from discord.ext.commands import Context
from runtime_yolk import Yolk


# Initialize runtime and bot client
runtime = Yolk(auto_load=True)
logger = runtime.get_logger(__name__)

intents = discord.Intents.default()
intents.presences = runtime.config.getboolean("INTENTS", "presences")
intents.members = runtime.config.getboolean("INTENTS", "members")
intents.message_content = runtime.config.getboolean("INTENTS", "message_content")
bot = commands.Bot(command_prefix="!", intents=intents)


async def is_correct_guild(ctx: Context) -> bool:
    """Check that command is run in correct guild."""
    return ctx.guild.id == runtime.config.getint("GUILD", "id")


@bot.listen()
async def on_command_error(ctx: Context, error: CommandError) -> None:
    """Handle command error."""
    logger.warning("Error captured in %s - %s", ctx.guild.id, error)


@bot.listen()
async def on_ready() -> None:
    """Simple console logging indicating ready event has fired."""
    guilds = [guild.name for guild in bot.guilds]
    logger.info("Eggbot has successfully loaded. In %s as %s", guilds, bot.user.id)


@bot.command()
@commands.check(is_correct_guild)
async def hello(ctx: Context) -> None:
    logger.info("Eggbot hello command recieved. Hello there!")
    await ctx.channel.send(f"Hello to you as well, {ctx.author.mention}!")


@bot.command()
@commands.check(is_correct_guild)
async def shutdown(ctx: Context) -> None:
    logger.info("Eggbot shutdown command recieved.  Until next time, space cowboy.")
    await ctx.channel.send(f"See you next time, {ctx.author.mention}.")
    await bot.close()


def main() -> int:
    bot.run(runtime.config.get("DEFAULT", "discord_token"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
