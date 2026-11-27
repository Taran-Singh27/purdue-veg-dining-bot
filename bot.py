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

def format_menu(menu_data):
    if type(menu_data) == str:
        return menu_data

    if len(menu_data) == 0:
        return "This dining court might be closed for this meal."

    formatted_data = ""
    for station, items in menu_data.items():
        formatted_data += f"**{station}**\n"
        if len(items) == 0:
            formatted_data += "- None\n"
        else:
            for item in items:
                formatted_data += f"- {item}\n"
        formatted_data += "\n"
    return formatted_data


@bot.command()
async def breakfast(ctx, location):
    breakfast_list = find_food_location(location.title(), "Breakfast")
    formatted_breakfast = format_menu(breakfast_list)
    await ctx.send(formatted_breakfast)

@bot.command()
async def lunch(ctx, location):
    lunch_list = find_food_location(location.title(), "Lunch")
    formatted_lunch = format_menu(lunch_list)
    await ctx.send(formatted_lunch)

@bot.command()
async def dinner(ctx, location):
    dinner_list = find_food_location(location.title(), "Dinner")
    formatted_dinner = format_menu(dinner_list)
    await ctx.send(formatted_dinner)

bot.run(TOKEN)
