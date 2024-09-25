from django.db.models import Max
from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import Entry, Country, Weather


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
    max_cost = entries.aggregate(Max('cost'))['cost__max'] or 0
    currencies = set(entry.currency.strip() for entry in entries)

    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')
    rating = request.GET.get('rating')
    selected_country = request.GET.get('country')
    selected_place = request.GET.get('place')
    selected_cost = request.GET.get('cost')
    selected_currency = request.GET.get('currency')
    selected_weather = request.GET.getlist('weather')
    selected_transport = request.GET.getlist('transport')

    if arrival_date:
        entries = entries.filter(arrival_date=arrival_date)
    if departure_date:
        entries = entries.filter(departure_date=departure_date)
    if rating:
        entries = entries.filter(rating=rating)
    if selected_country:
        entries = entries.filter(country__country=selected_country)
    if selected_place:
        entries = entries.filter(place__place=selected_place)
    if selected_cost:
        entries = entries.filter(cost__lte=selected_cost)
    if selected_currency:
        entries = entries.filter(currency=selected_currency)
    if selected_weather:
        entries = entries.filter(weather__type__in=selected_weather)
    if selected_transport:
        entries = entries.filter(transport__type__in=selected_transport)


    return render(request, 'entries.html', {
        'entries': entries,
        'countries': countries,
        'places': places,
        'max_cost': max_cost,
        'selected_cost': selected_cost,
        'currencies': list(currencies),
    })
