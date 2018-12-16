from django.db import models

class Portfolio(models.Model):
    password = models.CharField(max_length=300)

class Cryptocurrency(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    coin_symbol = models.CharField(max_length=10)
    coin_amount = models.FloatField(default=0.0)
    coin_investment = models.FloatField(default=0.0)
