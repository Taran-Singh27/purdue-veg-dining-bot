import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from menu import find_food_location

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def breakfast(ctx, location):
    breakfast_list = find_food_location(location.title(), "Breakfast")
    await ctx.send(breakfast_list)

@bot.command()
async def lunch(ctx, location):
    lunch_list = find_food_location(location.title(), "Lunch")
    await ctx.send(lunch_list)

@bot.command()
async def dinner(ctx, location):
    dinner_list = find_food_location(location.title(), "Dinner")
    await ctx.send(dinner_list)

bot.run(TOKEN)
