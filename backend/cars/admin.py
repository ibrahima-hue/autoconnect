from django.contrib import admin
from .models import Car, Seller, Appointment, Favorite


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ['name', 'seller_type', 'rating', 'is_verified', 'location']
    list_filter = ['seller_type', 'is_verified']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['make', 'model', 'year', 'price', 'fuel', 'seller', 'is_available']
    list_filter = ['fuel', 'transmission', 'is_available', 'year']
    search_fields = ['make', 'model', 'location']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['car', 'buyer', 'seller', 'date', 'time', 'status']
    list_filter = ['status', 'date']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'car', 'created_at']
