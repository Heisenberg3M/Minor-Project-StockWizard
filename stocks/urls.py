from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stocks-home'),
    path('<str:tid>', views.ticker, name='stocks-home'),
    path('historical/', views.historical, name='stocks-historical'),
    path('prediction/', views.prediction, name='stocks-prediction'),
    path('watchlist/', views.watchlist, name='stocks-watchlist'),
    path('about/', views.about, name='stocks-about')
]
