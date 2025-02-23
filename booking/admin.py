from django.contrib import admin
from .models import User, Location, Booking

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', 'cost', "capacity", 'description')
    search_fields = ('title', 'cost', "capacity")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'start_date', 'created_at', 'end_field')
    list_filter = ('start_date', 'location')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('User')
    search_fields = ('User')
    # тут хз если честно
