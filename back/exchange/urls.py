from django.urls import path
from .views import ExchangeList
from . import views
urlpatterns = [
    path('', ExchangeList.as_view(), name='exchange-list'),
    path('get_exchange_data/',views.get_exchange_data)
]
