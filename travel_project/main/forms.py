from django import forms
from .models import WeeklyOffer

class WeeklyOfferForm(forms.ModelForm):
    class Meta:
        model = WeeklyOffer
        fields = ['title', 'description', 'price', 'bookings', 'days',
                  'includes_flight', 'includes_hotel', 'includes_excursions', 'image', 'destination']
