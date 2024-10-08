from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from viewer.forms import EntryCreateForm
from viewer.models import Entry, Country, Weather, Place, Hashtag

def home(request):
    return render(request, "home.html")

class EntriesList(ListView):
    template_name = "entries.html"
    model = Entry
    context_object_name = 'entries'

def get_countries_and_places():
    countries = Country.objects.all()
    places = Place.objects.all()
    return countries, places

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
    hashtags_str = request.GET.get('hashtags')

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

    if hashtags_str:
        hashtags = hashtags_str.split(',')
        entries = entries.filter(hashtag__hashtag__in=hashtags).distinct()

    return render(request, 'entries.html', {
        'entries': entries,
        'countries': countries,
        'places': places,
        'max_cost': max_cost,
        'selected_cost': selected_cost,
        'currencies': list(currencies),
    })

class EntryCreateView(CreateView):
    template_name = 'entry_form.html'
    form_class = EntryCreateForm
    success_url = reverse_lazy('entries')

    def form_valid(self, form):
        return super().form_valid(form)

class EntryUpdateView(UpdateView):
    template_name = 'entry_form.html'
    model = Entry
    form_class = EntryCreateForm
    success_url = reverse_lazy('entries')

    def form_valid(self, form):
        return super().form_valid(form)

class EntryDeleteView(DeleteView):
    template_name = 'entry_delete.html'
    model = Entry
    success_url = reverse_lazy('entries')

class EntryDetailView(DetailView):
    template_name = 'entry.html'
    model = Entry
    context_object_name = 'entry'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object

        if entry.arrival_date and entry.departure_date:
            duration = (entry.departure_date - entry.arrival_date).days
        else:
            duration = None

        context['stayed_for'] = duration
        return context
