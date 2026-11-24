
from datetime import datetime, timedelta

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import RestaurantTable, Reservation


RESERVATION_DURATION = timedelta(hours=2)


# ==========================================
# RESERVATION VALIDATION
# ==========================================

class ReservationAdminForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get("date")
        time = cleaned_data.get("time")
        table = cleaned_data.get("table")
        status = cleaned_data.get("status")
        guests = cleaned_data.get("guests")

        if not all([date, time, table, status, guests]):
            return cleaned_data

        if status == "cancelled":
            return cleaned_data

        if not table.is_active:
            raise ValidationError(
                "This table is currently inactive."
            )

        if guests > table.capacity:
            raise ValidationError(
                f"Table {table.number} can accommodate "
                f"only {table.capacity} guests."
            )

        requested_start = datetime.combine(date, time)
        requested_end = (
            requested_start + RESERVATION_DURATION
        )

        existing_reservations = Reservation.objects.filter(
            table=table,
            status__in=["pending", "confirmed"],
            date__range=(
                (requested_start - RESERVATION_DURATION).date(),
                requested_end.date(),
            ),
        )

        if self.instance.pk:
            existing_reservations = existing_reservations.exclude(
                pk=self.instance.pk
            )

        for booking in existing_reservations:

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
                raise ValidationError(
                    f"Table {table.number} is already booked "
                    f"on {booking.date} at "
                    f"{booking.time.strftime('%H:%M')}. "
                    "Please select another table or time."
                )

        return cleaned_data


# ==========================================
# RESTAURANT TABLES
# ==========================================

@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "number",
        "capacity",
        "is_active",
    )

    list_display_links = (
        "id",
        "number",
    )

    list_editable = (
        "capacity",
        "is_active",
    )

    list_filter = (
        "capacity",
        "is_active",
    )

    search_fields = (
        "number__exact",
    )

    ordering = ("number",)

    list_per_page = 20


# ==========================================
# RESERVATIONS
# ==========================================

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):

    form = ReservationAdminForm

    list_display = (
        "id",
        "name",
        "date",
        "time",
        "guests",
        "table",
        "phone",
        "status",
        "created_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    # Status editing is done in the detail page
    # so validation cannot be bypassed.
    list_editable = ()

    list_filter = (
        "status",
        "date",
        "table",
        "created_at",
    )

    search_fields = (
        "name",
        "email",
        "phone",
    )

    ordering = (
        "date",
        "time",
    )

    list_per_page = 25

    readonly_fields = (
        "created_at",
    )

    fieldsets = (
        (
            "Guest Information",
            {
                "fields": (
                    "name",
                    "email",
                    "phone",
                )
            },
        ),
        (
            "Reservation Details",
            {
                "fields": (
                    "date",
                    "time",
                    "guests",
                    "table",
                    "notes",
                )
            },
        ),
        (
            "Reservation Status",
            {
                "fields": ("status",)
            },
        ),
        (
            "System Information",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    actions = (
        "cancel_reservations",
    )

    @admin.action(
        description="Cancel selected reservations"
    )
    def cancel_reservations(self, request, queryset):

        updated = queryset.update(
            status="cancelled"
        )

        self.message_user(
            request,
            f"{updated} reservation(s) cancelled.",
            level=messages.SUCCESS,
        )


from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'event_type',
        'date',
        'time',
        'is_active',
    )

    list_filter = (
        'event_type',
        'date',
        'is_active',
    )

    search_fields = (
        'title',
        'description',
    )

    list_editable = (
        'is_active',
    )

    ordering = (
        'date',
        'time',
    )
