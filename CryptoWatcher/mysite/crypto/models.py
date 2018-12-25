from django.db import models
from django.contrib.auth.models import User

import json
import requests

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    name = models.CharField(max_length=50, default="Crypto portfolio")
    def  __str__(self):
        return self.name

class Cryptocurrency(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    coin_symbol = models.CharField(max_length=10)
    coin_amount = models.FloatField(default=0.0)
    coin_investment = models.FloatField(default=0.0)
    def __str__(self):
        return self.coin_symbol
    def break_even_price(self):
        if self.coin_investment/self.coin_amount > 1:
            return "%.1f"% (self.coin_investment/self.coin_amount)
        else:
            return "%.3f" % (self.coin_investment/self.coin_amount)
    def price(self):
        coin_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+self.coin_symbol+"&tsyms=USD")
        coin = json.loads(coin_request.content)
        return coin['RAW'][self.coin_symbol]['USD']['PRICE']
    def worth(self):
        return "%.2f" % (self.coin_amount * self.price())
