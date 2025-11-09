import json
import os

class Portfolio:
    def __init__(self, cash):
        self.cash = cash
        self.positions = {}
        self.value = cash

    def buy(self, symbol, price, qty):
        cost = price * qty
        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + qty
            return f"🟢 Achat {qty:.2f} {symbol} à {price:.2f}$"
        return "❌ Fonds insuffisants"

    def sell(self, symbol, price):
        if symbol in self.positions:
            qty = self.positions.pop(symbol)
            proceeds = qty * price
            self.cash += proceeds
            return f"🔴 Vente {qty:.2f} {symbol} à {price:.2f}$"
        return "❌ Pas de position ouverte"

    def get_value(self, price):
        total = self.cash
        for symbol, qty in self.positions.items():
            total += qty * price
        self.value = total
        return total

    def save(self, path="data/portfolio.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump({
                "cash": self.cash,
                "positions": self.positions,
                "value": self.value
            }, f, indent=4)
