
from menu.models import Category, Dish
from django.contrib import messages
from .forms import ReservationForm
from django.shortcuts import render, redirect
from .models import Event
def home(request):
    featured_dish = (
        Dish.objects
        .filter(is_featured=True, is_available=True)
        .order_by('id')
        .first()
    )

    return render(request, 'core/home.html', {
        'featured_dish': featured_dish
    })


def menu(request):
    categories = Category.objects.prefetch_related('dishes').all()

    selected_category = request.GET.get('category')

    if selected_category:
        categories = categories.filter(id=selected_category)

    context = {
        'categories': categories,
        'all_categories': Category.objects.all(),
        'selected_category': selected_category,
    }

    return render(request, 'core/menu.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    return render(request, 'core/contact.html')



from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import ReservationForm
from .services import create_reservation


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)

        if form.is_valid():
            booking = create_reservation(form)

            if booking:
                messages.success(
                    request,
                    "Your reservation request has been received!"
                )
                return redirect("reservation")

            messages.error(
                request,
                "No tables are available for this time. "
                "Please choose another date or time."
            )
    else:
        form = ReservationForm()

    return render(
        request,
        "core/reservation.html",
        {"form": form},
    )


def cart(request):
    return render(request, 'core/cart.html')


from django.shortcuts import render
from django.utils import timezone


def events(request):

    today = timezone.localdate()

    upcoming_events = Event.objects.filter(
        is_active=True,
        date__gte=today
    ).order_by('date', 'time')

    context = {
        'events': upcoming_events,
    }

    return render(
        request,
        'core/events.html',
        context
    )



def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')
