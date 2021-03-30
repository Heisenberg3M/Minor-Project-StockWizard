from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='stocks-home'),
    path('<str:tid>', views.ticker, name='stocks-home'),
    path('about/', views.about, name='stocks-about')
]
