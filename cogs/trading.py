from discord.ext import commands, tasks
import asyncio
import yfinance as yf
import pandas as pd
from utils.portfolio import Portfolio
from config import INITIAL_CASH, SYMBOL, CHANNEL_ID
import joblib
import numpy as np

class Trading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.symbol = SYMBOL
        self.channel_id = CHANNEL_ID
        self.portfolio = Portfolio(INITIAL_CASH)
        self.model = joblib.load("data/model.pkl") if joblib.os.path.exists("data/model.pkl") else None

    def get_data(self):
        df = yf.download(self.symbol, period="1mo", interval="1d", progress=False)
        df["return"] = df["Close"].pct_change()
        df["ma5"] = df["Close"].rolling(5).mean()
        df["ma20"] = df["Close"].rolling(20).mean()
        df = df.dropna()
        return df

    def make_decision(self, df, sentiment_score):
        features = df[["return", "ma5", "ma20"]].iloc[-1:].values
        proba = self.model.predict_proba(features)[0][1]
        if proba > 0.6 and sentiment_score > 0.2:
            return "BUY", proba
        elif proba < 0.4 and sentiment_score < -0.2:
            return "SELL", proba
        else:
            return "HOLD", proba

    @tasks.loop(hours=1)
    async def auto_trade(self):
        channel = self.bot.get_channel(self.channel_id)
        df = self.get_data()
        price = df["Close"].iloc[-1]
        # Appel du cog de sentiment
        sentiment_cog = self.bot.get_cog("Sentiment")
        sentiment = sentiment_cog.get_sentiment(self.symbol)
        decision, proba = self.make_decision(df, sentiment)

        msg = f"📊 {self.symbol} | prix: {price:.2f} | proba hausse: {proba:.2f} | sentiment: {sentiment:+.2f} → {decision}"
        if decision == "BUY":
            msg += "\n" + self.portfolio.buy(self.symbol, price, self.portfolio.cash / price)
        elif decision == "SELL":
            msg += "\n" + self.portfolio.sell(self.symbol, price)

        self.portfolio.get_value(price)
        self.portfolio.save()
        await channel.send(msg)

    @commands.command()
    async def start(self, ctx):
        await ctx.send("🚀 Démarrage du trading automatique...")
        self.auto_trade.start()

async def setup(bot):
    await bot.add_cog(Trading(bot))
