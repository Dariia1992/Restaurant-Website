
from django.contrib import admin
from .models import Category, Dish


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'is_available',
    )
    list_display_links = ('id', 'name')
    list_editable = ('price', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('name', 'description')
    ordering = ('name',)
    list_per_page = 20
