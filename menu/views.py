from django.shortcuts import render

# Create your views here.
from menu.models import Dish, Category

def menu(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(is_available=True)

    context = {
        'categories': categories,
        'dishes': dishes,
    }

    return render(request, 'core/menu.html', context)