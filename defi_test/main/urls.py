from django.urls import path

from .views import get_balance, get_balance_batch, get_token_info

urlpatterns = [
    path('get_balance/', get_balance, name='get_balance'),
    path('get_balance_batch/', get_balance_batch, name='get_balance_batch'),
    path('get_token_info/', get_token_info, name='get_token_info'),
]
