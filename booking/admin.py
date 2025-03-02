from django.contrib import admin
from .models import User, Location, Booking

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', "capacity", 'description')
    search_fields = ('title', 'cost', "capacity")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'start_date', 'created_at', 'end_date')
    list_filter = ('start_date', 'location')
