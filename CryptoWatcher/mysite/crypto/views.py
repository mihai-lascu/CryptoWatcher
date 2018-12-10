from django.shortcuts import render

import json
import requests

#my_api_key-->&api_key=(4a6fae42c3f554998ee78a205df72209060cb6ce2c616dcefba56d9450f98f06)

def home(request):
    #Grab the crypto_list
    crypto_list_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,XLM,EOS,LTC,TRX,ADA,XMR,MIOTA,XEM,DASH,ETC&tsyms=USD")
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
            portfolio_password = request.POST['portfolio_password']
        except:
            return render(request, 'crypto/portfolio.html', {'portfolio_id': portfolio_id})
        else:
            return render(request, 'crypto/portfolio.html', {'portfolio_id': portfolio_id, 'portfolio_password': portfolio_password})
    else:
        notfound = "Portfolio feature coming soon"
        return render(request, 'crypto/portfolio.html', {'notfound': notfound })
