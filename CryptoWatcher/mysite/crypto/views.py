from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from passlib.hash import pbkdf2_sha256

from .models import Portfolio, Cryptocurrency

import json
import requests

#my_api_key-->&api_key=(4a6fae42c3f554998ee78a205df72209060cb6ce2c616dcefba56d9450f98f06)

def home(request):
    #Grab the crypto_list
    crypto_list_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,EOS,XLM,LTC,TRX,ADA,XMR,IOT,DASH,XEM,ETC&tsyms=USD")
    crypto_list = json.loads(crypto_list_request.content)

    #Grab the news
    news_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    news = json.loads(news_request.content)
    return render(request, 'crypto/home.html', {'news': news, 'crypto_list': crypto_list})

def prices(request):
    quote = request.POST['quote']
    coin_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+quote.upper()+"&tsyms=USD")
    coin = json.loads(coin_request.content)
    return render(request, 'crypto/prices.html', {'quote': quote, 'coin': coin})

def portfolio(request):
    if request.method == 'POST':
        portfolio_id = request.POST['portfolio_id']
        try:
            portfolio = Portfolio.objects.get(pk=portfolio_id)
        except (KeyError, Portfolio.DoesNotExist):
            return render(request, 'crypto/portfolio.html', {'notfound':'Wrong portfolio ID. Try again.'})
        else:
            return HttpResponseRedirect(reverse('crypto:portfolio_edit', args=(portfolio.id,)))
    else:
        return render(request, 'crypto/portfolio.html', {})

def portfolioCreate(request):
    new_portfolio = Portfolio(password='')
    new_portfolio.save()
    return render(request, 'crypto/portfolio_create.html', {'new_portfolio': new_portfolio })

def portfolioEdit(request, portfolio_id):
    if request.method == 'POST':
        if 'new_password' in request.POST.keys():
            portfolio_password = request.POST['new_password']
            portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
            portfolio.password = pbkdf2_sha256.hash(portfolio_password)
            portfolio.save()
            return render(request, 'crypto/portfolio_edit.html', {'portfolio_id': portfolio_id, 'password_correct': True})
            #return HttpResponseRedirect(reverse('crypto:portfolio_edit', args=(portfolio.id,)))
        elif 'portfolio_password' in request.POST.keys():
            portfolio_password = request.POST['portfolio_password']
            portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
            if pbkdf2_sha256.verify(portfolio_password, portfolio.password):
                return render(request, 'crypto/portfolio_edit.html', {'portfolio_id': portfolio_id, 'password_correct': True})
            else:
                return render(request, 'crypto/portfolio_edit.html', {'portfolio_id': portfolio_id, 'password_incorrect': True})
    else:
        portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
        return render(request, 'crypto/portfolio_edit.html', {'portfolio_id': portfolio_id, 'type_password': 'You need to type your password'})
