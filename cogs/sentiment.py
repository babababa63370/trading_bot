from discord.ext import commands
import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import numpy as np

class Sentiment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

    def get_sentiment(self, symbol):
        url = f"https://news.google.com/search?q={symbol}+stock&hl=en&gl=US&ceid=US:en"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        headlines = [a.text for a in soup.select("a.DY5T1d")[:5]]
        if not headlines:
            return 0.0

        results = self.sentiment_analyzer(headlines)
        scores = []
        for r in results:
            if r["label"] == "LABEL_2":
                scores.append(r["score"])
            elif r["label"] == "LABEL_0":
                scores.append(-r["score"])
        return float(np.mean(scores))

    @commands.command()
    async def sentiment(self, ctx, symbol="AAPL"):
        score = self.get_sentiment(symbol)
        await ctx.send(f"📰 Sentiment {symbol} : {score:+.2f}")

async def setup(bot):
    await bot.add_cog(Sentiment(bot))
