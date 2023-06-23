from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = "coins"

urlpatterns = [
    path('coins/', views.coin_list, name='coin_list')
]

urlpatterns = format_suffix_patterns(urlpatterns)