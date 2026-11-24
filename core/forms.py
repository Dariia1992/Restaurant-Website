
from datetime import datetime

from django import forms
from django.utils import timezone

from .models import Reservation


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation

        fields = [
            "name",
            "email",
            "phone",
            "date",
            "time",
            "guests",
            "notes",
        ]

        widgets = {
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            ),
            "time": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"},
            ),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def clean_guests(self):
        guests = self.cleaned_data["guests"]

        if not 1 <= guests <= 8:
            raise forms.ValidationError(
                "Please select between 1 and 8 guests."
            )

        return guests

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get("date")
        time = cleaned_data.get("time")

        if date and time:
            reservation_datetime = datetime.combine(date, time)

            if timezone.is_naive(reservation_datetime):
                reservation_datetime = timezone.make_aware(
                    reservation_datetime,
                    timezone.get_current_timezone(),
                )

            if reservation_datetime <= timezone.now():
                raise forms.ValidationError(
                    "Please choose a future date and time."
                )

        return cleaned_data
