from django.shortcuts import render
from django.views.generic import ListView

from viewer.models import Entry


def home(request):
    return render(request, "home.html")

class EntriesList(ListView):
    template_name = "entries.html"
    model = Entry
    context_object_name = 'entries'