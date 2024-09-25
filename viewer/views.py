from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import Entry, Country


def home(request):
    return render(request, "home.html")

class EntriesList(ListView):
    template_name = "entries.html"
    model = Entry
    context_object_name = 'entries'


def entry_list(request):
    entries = Entry.objects.all()
    countries = Entry.objects.values_list('country__country', flat=True).distinct()
    places = Entry.objects.values_list('place__place', flat=True).distinct()

    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')
    rating = request.GET.get('rating')
    selected_country = request.GET.get('country')  # Přidáno pro filtrování podle země
    selected_place = request.GET.get('place')

    if arrival_date:
        entries = entries.filter(arrival_date=arrival_date)
    if departure_date:
        entries = entries.filter(departure_date=departure_date)
    if rating:
        entries = entries.filter(rating=rating)
    if selected_country:
        entries = entries.filter(country__country=selected_country)  # Filtr podle země
    if selected_place:
        entries = entries.filter(place__place=selected_place)

    return render(request, 'entries.html', {'entries': entries, 'countries': countries, 'places': places})
