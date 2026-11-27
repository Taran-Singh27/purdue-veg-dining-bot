import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from menu import find_food_location

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None, case_insensitive=True)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Please include a location, e.g. `!{ctx.command} wiley`")
    else:
        raise error

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Purdue Dining Bot Help",
        description="Check today's vegetarian menus across Purdue dining courts.",
        color=0xCEB888
    )
    embed.add_field(
        name="Commands",
        value="`!breakfast <location>` — Breakfast menu\n`!lunch <location>` — Lunch menu\n`!dinner <location>` — Dinner menu",
        inline=False
    )
    embed.add_field(
        name="Dining Courts",
        value="Earhart • Ford • Hillenbrand • Wiley • Windsor",
        inline=False
    )
    embed.set_footer(text="Example: !lunch wiley")
    await ctx.send(embed=embed)


def format_menu(menu_data, location, meal):
    if type(menu_data) == str:
        return discord.Embed(
            title="Error",
            description=menu_data,
            color=0xE74C3C
        )

    if len(menu_data) == 0:
        return discord.Embed(
            title=f"{location} — {meal}",
            description="This dining court might be closed for this meal.",
            color=0xCEB888
        )

    embed = discord.Embed(
        title=f"{location} — {meal}",
        color=0xCEB888
    )

    for station, items in menu_data.items():
        if len(items) == 0:
            continue  

        items_text = ""
        for item in items:
            items_text += f"• {item}\n"

        embed.add_field(name=station, value=items_text, inline=False)
    return embed


@bot.command()
async def breakfast(ctx, location):
    breakfast_list = find_food_location(location.title(), "Breakfast")
    formatted_breakfast = format_menu(breakfast_list, location.title(), "Breakfast")
    await ctx.send(embed=formatted_breakfast)

@bot.command()
async def lunch(ctx, location):
    lunch_list = find_food_location(location.title(), "Lunch")
    formatted_lunch = format_menu(lunch_list, location.title(), "Lunch")
    await ctx.send(embed=formatted_lunch)

@bot.command()
async def dinner(ctx, location):
    dinner_list = find_food_location(location.title(), "Dinner")
    formatted_dinner = format_menu(dinner_list, location.title(), "Dinner")
    await ctx.send(embed=formatted_dinner)

bot.run(TOKEN)
