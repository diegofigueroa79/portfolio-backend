from django.urls import path
from . import views

app_name = "coins"

urlpatterns = [
    path('coins/', views.coin_list, name='coin_list'),
    path('coins/<str:slug>/', views.coin_detail, name='coin_detail'),
    path('coins/history/<str:symbol>/<str:period>/', views.coin_detail_historical, name='coin_detail_historical')
]
