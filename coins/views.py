from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
import requests as r
import os


# Create your views here.
@api_view(['GET'])
def coin_list(request):
    """
    Fetch first 100 coins from CoinMarketCap.
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
