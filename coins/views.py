from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import requests as r
import os
from datetime import datetime, timedelta


# Create your views here.
@api_view(['GET'])
def coin_list(request):
    """
    Fetch first 10 coins from CoinMarketCap.
    List coins with relavent properties.
    """
    url = os.environ['CMC_API_DOMAIN'] + '/v1/cryptocurrency/listings/latest?limit=10'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY'],
    }
    try:
        response = r.get(url=url, headers=headers)
    except Exception as e:
        print(str(e))
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if response.ok:
            coins = []
            slugs = []
            data = response.json()['data']
            for item in data:
                coin = {}
                coin['id'] = item['id']
                coin['name'] = item['name']
                coin['symbol'] = item['symbol']
                coin['slug'] = item['slug']
                coin['circulating_supply'] = item['circulating_supply']
                coin['total_supply'] = item['total_supply']
                coin['max_supply'] = item['max_supply']
                coin['price'] = item['quote']['USD']['price']
                coin['percent_change_24h'] = item['quote']['USD']['percent_change_24h']
                coin['market_cap'] = item['quote']['USD']['market_cap']
                coin['logo'] = ""
                coins.append(coin)
                slugs.append(coin['slug'])
                slug_query = ",".join(slugs)
            
            url = f"{os.environ['CMC_API_DOMAIN']}/v2/cryptocurrency/info?slug={slug_query}&aux=logo"
            try:
                response = r.get(url=url, headers=headers)
            except Exception as e:
                print(str(e))
            else:
                if response.ok:
                    data = response.json()['data']
                    for coin in coins:
                        coin['logo'] = data[str(coin['id'])]['logo']
                    return Response(coins, status=status.HTTP_200_OK)
            return Response(coins, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def coin_detail(request, slug):
    """
    Fetch detail data of a coin from CMC.
    """
    coin = {}

    url = f"{os.environ['CMC_API_DOMAIN']}/v2/cryptocurrency/info?slug={slug}"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.environ['CMC_API_KEY'],
    }

    try:
        response = r.get(url=url, headers=headers)
    except Exception as e:
        print(str(e))
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if response.ok:
            data = response.json()['data']
            for item in data:
                coin['website'] = data[item]['urls']['website'][0]
                coin['id'] = item
                coin['slug'] = slug
                coin['name'] = data[item]['name']
                coin['symbol'] = data[item]['symbol']
                coin['description'] = data[item]['description']
                coin['logo'] = data[item]['logo']
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    
    url = f"{os.environ['CMC_API_DOMAIN']}/v2/cryptocurrency/quotes/latest?slug={slug}"

    try:
        response = r.get(url=url, headers=headers)
    except Exception as e:
        print(str(e))
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if response.ok:
            data = response.json()['data']
            for item in data:
                coin['circulating_supply'] = data[item]['circulating_supply']
                coin['max_supply'] = data[item]['max_supply']
                coin['price'] = data[item]['quote']['USD']['price']
                coin['percent_change_24h'] = data[item]['quote']['USD']['percent_change_24h']
                coin['volume'] = data[item]['quote']['USD']['volume_24h']
                coin['marketcap'] = data[item]['quote']['USD']['market_cap']
            
            return Response(coin, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def coin_detail_historical(request, symbol, period):
    """
    Fetch detail historical price data.
    Symbol is the cryptocurrency symbol, e.g. BTC
    Seriod is time unit per quote. Available periods:
    Second	1SEC, 2SEC, 3SEC, 4SEC, 5SEC, 6SEC, 10SEC, 15SEC, 20SEC, 30SEC
    Minute	1MIN, 2MIN, 3MIN, 4MIN, 5MIN, 6MIN, 10MIN, 15MIN, 20MIN, 30MIN
    Hour	1HRS, 2HRS, 3HRS, 4HRS, 6HRS, 8HRS, 12HRS
    Day	1DAY, 2DAY, 3DAY, 5DAY, 7DAY, 10DAY
    Month	1MTH, 2MTH, 3MTH, 4MTH, 6MTH
    Year	1YRS, 2YRS, 3YRS, 4YRS, 5YRS
    """
    if period == 'day':
        time_period = "1HRS"
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, microsecond=0)
    elif period == 'month':
        time_period = "1DAY"
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, microsecond=0)
        dt = dt - timedelta(30)
    elif period == 'year':
        time_period = "1DAY"
        dt = datetime.now()
        dt = dt.replace(hour=0, minute=0, microsecond=0)
        dt = dt - timedelta(365)

    url = f"{os.environ['COINAPI_DOMAIN']}/v1/ohlcv/BITSTAMP_SPOT_{symbol}_USD/history?period_id={time_period}&time_start={dt.isoformat()}"
    headers = {
        'Accepts': 'application/json',
        'X-CoinAPI-Key' : os.environ['COINAPI_KEY'],
    }

    try:
        response = r.get(url=url, headers=headers)
    except Exception as e:
        print(str(e))
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        if response.ok:
            data = response.json()
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
