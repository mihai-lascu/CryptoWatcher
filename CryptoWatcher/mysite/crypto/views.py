from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Portfolio, Cryptocurrency
from django.contrib.auth.models import User

import json
import requests

#my_api_key-->&api_key=(4a6fae42c3f554998ee78a205df72209060cb6ce2c616dcefba56d9450f98f06)

def home(request):
    crypto_list_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,EOS,XLM,LTC,TRX,ADA,IOT,XMR,DASH,XEM,ETC&tsyms=USD")
    crypto_list = json.loads(crypto_list_request.content)
    news_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    news = json.loads(news_request.content)
    return render(request, 'crypto/home.html', {'news': news, 'crypto_list': crypto_list})

def prices(request):
    quote = request.POST['quote']
    coin_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+quote.upper()+"&tsyms=USD")
    coin = json.loads(coin_request.content)
    return render(request, 'crypto/prices.html', {'quote': quote, 'coin': coin})

def portfolio(request):
    return render(request, 'crypto/portfolio.html')

@login_required
def portfolioProfile(request):
    current_user = request.user
    portfolios = current_user.portfolio_set.all()
    crypto_coins = {}
    #hard
    for p in portfolios:
        crypto_coins[p.id] = p.cryptocurrency_set.all()
    return render(request, 'crypto/portfolio_profile.html', { 'portfolios': portfolios, 'crypto_coins': crypto_coins })

@login_required
def portfolioEdit(request, portfolio_id):
    current_user = request.user
    try:
        portfolio = current_user.portfolio_set.get(pk=portfolio_id)
        crypto_coins = portfolio.cryptocurrency_set.all()
    except (KeyError, Portfolio.DoesNotExist):
        messages.info(request, "I'm sorry, that portfolio is not yours")
        return redirect('crypto:profile')
    else:
        if request.method == 'POST':
            if 'delete_portfolio' in request.POST.keys():
                portfolio.delete()
                messages.info(request, "Portfolio %s deleted" % portfolio.name)
                return redirect('crypto:profile')
            elif 'change_name' in request.POST.keys():
                portfolio.name = request.POST['change_name']
                portfolio.save()
                return redirect(reverse('crypto:edit', args=(portfolio.id,)))
            elif 'add_coin' in request.POST.keys():
                portfolio.cryptocurrency_set.create(coin_symbol=request.POST['coin_symbol'].upper(), coin_investment=request.POST['amount_invested'], coin_amount=request.POST['coin_amount'])
                return redirect(reverse('crypto:edit', args=(portfolio.id,)))
            elif 'remove_coin' in request.POST.keys():
                coin = portfolio.cryptocurrency_set.get(pk=request.POST['remove_coin'])
                coin.delete()
                return redirect(reverse('crypto:edit', args=(portfolio.id,)))
        else:
            return render(request, 'crypto/portfolio_edit.html', { 'portfolio': portfolio, 'crypto_coins': crypto_coins })

@login_required
def portfolioCreate(request):
    current_user = request.user
    portfolio = current_user.portfolio_set.create(user=current_user)
    portfolio.save()
    return redirect(reverse('crypto:edit', args=(portfolio.id,)))
