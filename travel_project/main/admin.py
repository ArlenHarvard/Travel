# main/admin.py
from django.contrib import admin
from .models import Destination, Place, WeeklyOffer


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ("title", "continent", "population_mil", "area_km2", "gdp_usd", "created_at")
    search_fields = ("title", "continent")
    list_filter = ("continent",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Place)

@admin.register(WeeklyOffer)
class WeeklyOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'destination', 'price', 'bookings', 'days', 'includes_flight', 'includes_hotel', 'includes_excursions')
    list_filter = ('destination', 'includes_flight', 'includes_hotel', 'includes_excursions')
    search_fields = ('title', 'destination__title')