from discord.ext import commands
import json

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wallet(self, ctx):
        with open("data/portfolio.json") as f:
            p = json.load(f)
        msg = f"💰 Cash: {p['cash']:.2f}$\n📦 Positions: {p['positions']}\n📈 Valeur totale: {p['value']:.2f}$"
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(Report(bot))
