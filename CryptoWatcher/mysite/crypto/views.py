from django.shortcuts import render

import json
import requests

#my_api_key-->&api_key=(4a6fae42c3f554998ee78a205df72209060cb6ce2c616dcefba56d9450f98f06)

def home(request):

    price_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms=BTC,XRP,ETH,XLM,EOS,LTC,TRX,XMR,ADA&tsyms=USD")
    price = json.loads(price_request.content)

    #Grab the news
    news_request = requests.get("https://min-api.cryptocompare.com/data/v2/news/?lang=EN")
    news = json.loads(news_request.content)
    return render(request, 'crypto/home.html', {'news': news, 'price': price})

def prices(request):
    if request.method == 'POST':
        quote = request.POST['quote']
        coin_request = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms="+quote.upper()+"&tsyms=USD")
        coin = json.loads(coin_request.content)
        return render(request, 'crypto/prices.html', {'quote': quote, 'coin': coin})
    else:
        notfound = "Enter a crypto currency into the form above"
        return render(request, 'crypto/prices.html', {'notfound': notfound })
