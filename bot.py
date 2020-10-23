import json
import random

import discord
from discord.ext import commands

aliens = open("alien_scrape.txt", 'r').read().split('\n\n\n')

alien_dict = {}
COLORS = frozenset(("Pink", "White", "Green", "Yellow", "Purple", "Red", "Blue", "Orange"))

for alien in aliens:
    (key, _) = alien.split('[')
    alien_dict[key.strip().lower()] = alien

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

MAX_MESSAGE_LENGTH = 2000
MAX_ALIEN_NAME_LENGTH = 50


def paginate_message(message):
    message_queue = []
    i = 0
    while i < len(message):
        j = i + MAX_MESSAGE_LENGTH
        if j > len(message):
            j = len(message)
        else:
            j = message[i:j].rfind('\n')
        message_queue.append(message[i:j])
        i = j
    return message_queue


@bot.command()
async def alien(ctx, *args):
    alien_name = " ".join(args).lower()
    if len(alien_name) == 0:
        await ctx.send("You didn't provide any alien name to query.")
        return
    if len(alien_name) > MAX_ALIEN_NAME_LENGTH:
        await ctx.send("Alien names would never be this long.")
        return
    if alien_name in alien_dict:
        message_queue = paginate_message(alien_dict[alien_name])
        for message in message_queue:
            await ctx.send(message)
    else:
        await ctx.send("Could not find alien named {alien_name}.".format(
            alien_name=alien_name))

@bot.command()
async def color(ctx, *args):
    if 3 <= len(args) <= 8:
        await ctx.send(", ".join(map(str, zip(args, random.sample(COLORS, len(args))))))
    else:
        await ctx.send(f"Having {len(args)} players is not within the 3-8 player ruleset")

@bot.command()
async def colors(ctx):
    players = [member.nick if member.nick is not None else member.name for voice_channel in ctx.guild.voice_channels for member in voice_channel.members]
    if 3 <= len(players) <= 8:
        await ctx.send(", ".join(map(str, zip(players, random.sample(COLORS, len(players))))))
    else:
        await ctx.send(f"Having {len(players)} players is not within the 3-8 player ruleset")


with open('./secret_config.json', 'r') as f:
    data = json.load(f)

bot.run(data["token"])
