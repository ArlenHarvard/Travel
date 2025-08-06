# main/views.py
from django.shortcuts import render, get_object_or_404
from .models import *
from django.core.paginator import Paginator


def index(request):
    destinations = Destination.objects.all()
    paginator = Paginator(destinations, 3)  # 3 записи на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "destinations": destinations[:4],  # первые 4 для баннеров
    }

    return render(request, "main/index.html", context)

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    places = destination.places.all()
    weekly_offers = WeeklyOffer.objects.filter(destination=destination).distinct()
    return render(request, "main/destination_detail.html", {
        "destination": destination,
        "weekly_offers": weekly_offers,
        "places": places,
    })


def about_view(request):
    return render(request, 'main/about.html')