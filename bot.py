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

DINING_COURTS = ["Earhart", "Ford", "Hillenbrand", "Wiley", "Windsor"]

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Purdue Dining Bot Help",
        description="Check today's vegetarian menus across Purdue dining courts.",
        color=0xCEB888
    )
    embed.add_field(
        name="Commands",
        value="`!breakfast [location]` — Breakfast menu\n`!lunch [location]` — Lunch menu\n`!dinner [location]` — Dinner menu",
        inline=False
    )
    embed.add_field(
        name="Dining Courts",
        value="Earhart • Ford • Hillenbrand • Wiley • Windsor",
        inline=False
    )
    embed.set_footer(text="Example: !lunch or !lunch wiley")
    await ctx.send(embed=embed)

async def send_menu(ctx, location, meal):
    if location is None:
        for court in DINING_COURTS:
            data = find_food_location(court, meal)
            embed = format_menu(data, court, meal)
            await ctx.send(embed=embed)
        return

    clean_location = location.title()
    if clean_location not in DINING_COURTS:
        valid = " • ".join(DINING_COURTS)
        embed = discord.Embed(
                    title=f"Unknown Location — `{location}`",
                    description=f"Try one of: {valid}",
                    color=0xE74C3C
                )
        await ctx.send(embed=embed)
        return

    data = find_food_location(clean_location, meal)
    embed = format_menu(data, clean_location, meal)
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
async def breakfast(ctx, location=None):
    await send_menu(ctx, location, "Breakfast")

@bot.command()
async def lunch(ctx, location=None):
    await send_menu(ctx, location, "Lunch")

@bot.command()
async def dinner(ctx, location=None):
    await send_menu(ctx, location, "Dinner")

bot.run(TOKEN)
