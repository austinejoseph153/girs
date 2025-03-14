from django.contrib import admin
from .models import Location, LocationCategory

@admin.register(Location)
class LocationModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'latitude', 'longitude','category')
    ordering = ["-id"]


@admin.register(LocationCategory)
class LocationCategoryModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

