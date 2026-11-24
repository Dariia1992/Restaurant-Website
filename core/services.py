
from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from .models import RestaurantTable, Reservation


RESERVATION_DURATION = timedelta(hours=2)


def find_available_table(date, time, guests):
    requested_start = datetime.combine(date, time)
    requested_end = requested_start + RESERVATION_DURATION

    tables = RestaurantTable.objects.filter(
        is_active=True,
        capacity__gte=guests,
    ).order_by("capacity", "number")

    # Check both the selected date and adjacent date,
    # in case a reservation crosses midnight.
    dates_to_check = [
        requested_start.date(),
        requested_end.date(),
        (requested_start - RESERVATION_DURATION).date(),
    ]

    bookings = Reservation.objects.filter(
        date__in=dates_to_check,
        status__in=["pending", "confirmed"],
        table__isnull=False,
    )

    occupied_ids = set()

    for booking in bookings:
        booking_start = datetime.combine(
            booking.date,
            booking.time,
        )

        booking_end = (
            booking_start + RESERVATION_DURATION
        )

        overlaps = (
            requested_start < booking_end
            and requested_end > booking_start
        )

        if overlaps:
            occupied_ids.add(booking.table_id)

    return tables.exclude(
        id__in=occupied_ids
    ).first()


def create_reservation(form):
    with transaction.atomic():
        # Serialize booking decisions for the same date
        # by locking the active table rows.
        list(
            RestaurantTable.objects
            .select_for_update()
            .filter(is_active=True)
            .order_by("id")
        )

        date = form.cleaned_data["date"]
        time = form.cleaned_data["time"]
        guests = form.cleaned_data["guests"]

        start = timezone.make_aware(
            datetime.combine(date, time),
            timezone.get_current_timezone(),
        )

        if start <= timezone.now():
            return None

        table = find_available_table(
            date,
            time,
            guests,
        )

        if table is None:
            return None

        reservation = form.save(commit=False)
        reservation.table = table
        reservation.status = "pending"
        reservation.save()

        return reservation
