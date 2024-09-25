from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import Entry


def home(request):
    return render(request, "home.html")

class EntriesList(ListView):
    template_name = "entries.html"
    model = Entry
    context_object_name = 'entries'

def entry_filtered_list(request):
    entries = Entry.objects.all()

    arrival_date = request.GET.get('arrival_date')
    departure_date = request.GET.get('departure_date')
    rating = request.GET.get('rating')

    if arrival_date:
        entries = entries.filter(arrival_date=arrival_date)
    if departure_date:
        entries = entries.filter(departure_date=departure_date)
    if rating:
        entries = entries.filter(rating=rating)

    return render(request, 'entries.html', {'entries': entries})