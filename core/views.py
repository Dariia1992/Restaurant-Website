
from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def menu(request):
    return render(request, 'core/menu.html')


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')


def reservation(request):
    return render(request, 'core/reservation.html')


def cart(request):
    return render(request, 'core/cart.html')


def events(request):
    return render(request, 'core/events.html')


def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')
