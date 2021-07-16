import signal
import sys

import mangoo_setup
mangoo_setup.global_init()

from discord.ext import commands

import prefix

bot = commands.Bot(command_prefix=prefix.prefix_get, help_command=None)


def signal_handler(sig, frame):
    print('\nBot killed by user')
    sys.exit(0)


@bot.event
async def on_ready():
    print("Bot is ready")


@bot.command()
async def reload(ctx, name):
    bot.reload_extension(f"{name}")


def run():
    signal.signal(signal.SIGINT, signal_handler)
    bot.load_extension("economy")
    bot.load_extension("general")
    bot.load_extension("prefix")
    bot.run('token')


run()
