import discord
from discord.ext import commands
import os
from config import TOKEN

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Chargement automatique des cogs
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and not filename.startswith("__"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"🧩 Cog chargé : {filename}")

bot.run(TOKEN)
