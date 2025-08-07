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


from django.shortcuts import render
from .models import WeeklyOffer, Destination

def weekly_deals_view(request):
    offers = WeeklyOffer.objects.select_related('destination').all()

    # Получаем уникальные направления из всех офферов
    destinations = Destination.objects.filter(weekly_offers__in=offers).distinct()

    destination_slug = request.GET.get('destination')
    price_range = request.GET.get('price_range')

    if destination_slug:
        offers = offers.filter(destination__slug=destination_slug)

    if price_range:
        try:
            if price_range == "2500+":
                offers = offers.filter(price__gte=2500)
            else:
                min_price, max_price = map(int, price_range.split('-'))
                offers = offers.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    return render(request, 'main/deals.html', {
        'offers': offers,
        'destinations': destinations,
    })


def reservation_view(request):
    return render(request, 'main/reservation.html')
