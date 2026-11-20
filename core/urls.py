from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('reservation/', views.reservation, name='reservation'),
    path('cart/', views.cart, name='cart'),
    path('events/', views.events, name='events'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]
