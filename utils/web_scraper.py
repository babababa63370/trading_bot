import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import numpy as np

class WebSentiment:
    def __init__(self):
        self.analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

    def get_headlines(self, symbol: str, limit: int = 5):
        """Scrape Google News pour un ticker."""
        url = f"https://news.google.com/search?q={symbol}+stock&hl=en&gl=US&ceid=US:en"
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        return [a.text for a in soup.select("a.DY5T1d")[:limit]]

    def compute_sentiment(self, headlines):
        """Retourne un score de sentiment entre -1 et +1."""
        if not headlines:
            return 0.0
        results = self.analyzer(headlines)
        scores = []
        for r in results:
            if r["label"] == "LABEL_2":  # positif
                scores.append(r["score"])
            elif r["label"] == "LABEL_0":  # négatif
                scores.append(-r["score"])
        return float(np.mean(scores)) if scores else 0.0

    def get_sentiment(self, symbol):
        headlines = self.get_headlines(symbol)
        return self.compute_sentiment(headlines)
