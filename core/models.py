
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RestaurantTable(models.Model):
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["number"]

    def __str__(self):
        return f"Table {self.number} — {self.capacity} guests"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30)

    date = models.DateField()
    time = models.TimeField()

    guests = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(8),
        ]
    )

    table = models.ForeignKey(
        RestaurantTable,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="reservations",
    )

    notes = models.TextField(blank=True)

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="pending",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.date} {self.time}"



from django.db import models


class Event(models.Model):

    EVENT_TYPES = [
        ('live_music', 'Live Music'),
        ('special_dinner', 'Special Dinner'),
        ('workshop', 'Workshop'),
        ('tasting', 'Tasting'),
        ('other', 'Other'),
    ]

    title = models.CharField(
        max_length=150,
        verbose_name='Event Title'
    )

    event_type = models.CharField(
        max_length=30,
        choices=EVENT_TYPES,
        default='other',
        verbose_name='Event Type'
    )

    description = models.TextField(
        blank=True,
        verbose_name='Description'
    )

    date = models.DateField(
        verbose_name='Event Date'
    )

    time = models.TimeField(
        verbose_name='Start Time'
    )

    image = models.ImageField(
        upload_to='events/',
        blank=True,
        null=True,
        verbose_name='Event Image'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='Show on Website'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['date', 'time']
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return f'{self.title} — {self.date}'
