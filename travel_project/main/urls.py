# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("destination/<slug:slug>/", views.destination_detail, name="destination_detail"),
    path('about/', views.about_view, name='about'),
    path('deals/', views.weekly_deals_view, name='deals'),
    path('reservation/', views.reservation_view, name='reservation'),
]
