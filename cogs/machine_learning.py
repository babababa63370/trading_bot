from discord.ext import commands
import yfinance as yf
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class MachineLearning(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model_path = "data/model.pkl"
        self.model = None
        self.symbol = "AAPL"

    def train_model(self):
        df = yf.download(self.symbol, period="6mo", interval="1d", progress=False)
        df["return"] = df["Close"].pct_change()
        df["ma5"] = df["Close"].rolling(5).mean()
        df["ma20"] = df["Close"].rolling(20).mean()
        df = df.dropna()
        df["target"] = (df["Close"].shift(-1) > df["Close"]).astype(int)

        X = df[["return", "ma5", "ma20"]]
        y = df["target"]

        model = RandomForestClassifier(n_estimators=100)
        model.fit(X, y)
        joblib.dump(model, self.model_path)
        self.model = model
        return f"✅ Modèle entraîné sur {len(X)} échantillons"

    def predict(self, df):
        if self.model is None:
            if os.path.exists(self.model_path):
                self.model = joblib.load(self.model_path)
            else:
                self.train_model()
        features = df[["return", "ma5", "ma20"]].iloc[-1:].values
        return self.model.predict_proba(features)[0][1]

    @commands.command()
    async def retrain(self, ctx):
        msg = self.train_model()
        await ctx.send(msg)

async def setup(bot):
    await bot.add_cog(MachineLearning(bot))
