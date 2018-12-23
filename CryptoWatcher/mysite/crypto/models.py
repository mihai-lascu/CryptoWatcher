from django.db import models
from django.contrib.auth.models import User

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
