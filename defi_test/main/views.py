import json

import requests
from defi_test.settings import POLYGON_API_KEY
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET'])
def get_balance(request):
    """Get the token address, query the endpoint to get the balance, divide and round to one decimal place"""

    data_token_address = request.data.get('token_address')

    polygon_request = requests.get(f'https://api.polygonscan.com/api?module=account&action=balance'
                                   f'&address={data_token_address}'
                                   f'&apikey={POLYGON_API_KEY}')

    response = polygon_request.json()
    balance = round(int(response.get('result')) / 10000000000000000, 1)
    data = {'balance': balance}
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_balance_batch(request):
    """Get the address of the tokens, query the endpoint to get the balance, divide and round to one decimal place"""

    data_token_address_batch = request.data.get('token_address_batch')
    data_token_address_batch_convert = json.loads(data_token_address_batch)
    token_address_batch = ','.join(data_token_address_batch_convert)

    polygon_request = requests.get(f'https://api.polygonscan.com/api?module=account&action=balancemulti'
                                   f'&address={token_address_batch}'
                                   f'&apikey={POLYGON_API_KEY}')
    response = polygon_request.json()
    balances = [round(int(balance.get('balance')) / 10000000000000000, 1) for balance in response.get('result')]
    data = {'balances': balances}

    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_token_info(request):
    """
    Get the address of the token, query the endpoint to get information about the token, and then display this
    information to the user
    """
    data_token_address = request.data.get('token_address')

    polygon_request = requests.get(f'https://api.polygonscan.com/api?module=token'
                                   f'&action=tokeninfo'
                                   f'&contractaddress={data_token_address}'
                                   f'&apikey={POLYGON_API_KEY}')

    token_info = polygon_request.json().get('result')[0]

    data = {'symbol': token_info.get('symbol'), 'name': token_info.get('tokenName'),
            'totalSupply': int(round(float(token_info.get('totalSupply')), 0))}
    return JsonResponse(data, safe=False, status=status.HTTP_200_OK)
