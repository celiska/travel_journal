from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Max
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User

from viewer.forms import EntryCreateForm, ImageUploadForm
from viewer.models import Entry, Country, Place, Image


def home(request):
    return render(request, "home.html")


class EntriesEditView(UserPassesTestMixin, ListView):
    template_name = "edit_panel.html"
    model = Entry
    context_object_name = 'entries_list'


    def test_func(self):
        """Page will be shown only to users with editor privileges or to administrators"""
        return self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()


class EntryCreateView(LoginRequiredMixin, CreateView):
    template_name = 'entry_form.html'
    form_class = EntryCreateForm

    def form_valid(self, form):
        """Upon receiving a valid post request, the current user will be added to the new entry's author field.
        The user will then be directed to upload images
        """
        form.instance.author = self.request.user
        entry = form.save()
        return redirect(reverse('image_upload', kwargs={'pk': entry.pk}))


class EntryUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'entry_form.html'
    model = Entry
    form_class = EntryCreateForm

    def test_func(self):
        """Page will only be shown to the entry's author or to users with editor privileges"""
        entry = self.get_object()
        is_editor_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()
        return entry.author == self.request.user or is_editor_or_superuser

    def get_context_data(self, **kwargs):
        """This allows already existing places and hashtags to show up on the update page"""
        context = super().get_context_data(**kwargs)
        entry = self.object
        context['saved_places'] = entry.place.all()
        context['saved_countries'] = entry.country.all()
        context['saved_hashtags'] = entry.hashtag.all()
        return context

    def form_valid(self, form):
        """Upon successful update, the image upload page will be shown"""
        entry = form.save()
        return redirect(reverse('image_upload', kwargs={'pk': entry.pk}))


class EntryDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'entry_delete.html'
    model = Entry
    success_url = reverse_lazy('entries')

    def test_func(self):
        """Page will only be shown to the entry's author or to users with editor privileges"""
        entry = self.get_object()
        is_editor_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()
        return entry.author == self.request.user or is_editor_or_superuser

class EntryDetailView(UserPassesTestMixin, DetailView):
    template_name = 'entry_detail.html'
    model = Entry
    context_object_name = 'entry'

    def test_func(self):
        """Entries marked as private will only be shown to the entry's author or to users with editor privileges"""
        entry = self.get_object()
        is_editor_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()
        return not entry.is_private or entry.author == self.request.user or is_editor_or_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        entry = self.object

        # If an entry has both an arrival and departure date, the duration of the trip is calculated
        if entry.arrival_date and entry.departure_date:
            duration = (entry.departure_date - entry.arrival_date).days
        else:
            duration = None

        # FontAwesome icons to be shown for each weather and transport selection
        weather_icons = {
            "overcast": "cloud",
            "rain": "cloud-rain",
            "sun": "sun",
            "storm": "bolt",
            "wind": "wind",
            "snow": "snowflake",
            "fog": "smog",
            "hail": "cloud-meatball",
            "chill": "temperature-low",
            "hot": "temperature-high"
        }

        transport_icons = {
            "plane": "plane",
            "train": "train",
            "metro": "train-subway",
            "tram": "train-tram",
            "car": "car",
            "bus": "bus",
            "cable_car": "cable-car",
            "on_foot": "person-walking",
            "boat": "sailboat",
            "bicycle": "bicycle",
            "motorcycle": "motorcycle",
            "horse": "horse"
        }

        weather_icon_list = []
        for weather in entry.weather.all():
            weather_icon_list.append(weather_icons.get(weather.type, "question"))

        transport_icon_list = []
        for transport in entry.transport.all():
            transport_icon_list.append(transport_icons.get(transport.type, "question"))

        context['stayed_for'] = duration
        context['weather_icon_list'] = weather_icon_list
        context['transport_icon_list'] = transport_icon_list

        return context

def get_countries_and_places():
    countries = Country.objects.all()
    places = Place.objects.all()
    return countries, places

def get_filtered_entries(request):
    """Used by the filter function in the 'view trips' view"""
    entries = Entry.objects.filter(is_private=False).distinct()

    countries = entries.values_list('country__country', flat=True).distinct()
    places = entries.values_list('place__place', flat=True).distinct()
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

def search_results(request):
    query = request.GET.get('query')
    if query:
        entry_results = Entry.objects.filter(is_private=False).filter(
            entry_name__icontains=query
        ) | Entry.objects.filter(is_private=False).filter(
            description__icontains=query
        )
        user_results = User.objects.filter(username__icontains=query) | User.objects.filter(
            profile__display_name__icontains=query
        )
    else:
        entry_results = Entry.objects.none()
        user_results = User.objects.none()

    return render(request, 'search_results.html', {
        'entry_results': entry_results,
        'user_results': user_results,
        'query': query
    })


class ImageUploadView(UserPassesTestMixin, CreateView):
    template_name = 'image_upload.html'
    form_class = ImageUploadForm

    def test_func(self):
        """Page will only be shown to the entry's author or to users with editor privileges"""
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        is_editor_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()
        return entry.author == self.request.user or is_editor_or_superuser

    def get_success_url(self):
        """Upon upload, user will stay on the upload page to upload more photos"""
        return reverse_lazy('image_upload', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        """Shows data relating to the entry associated with the images being uploaded"""
        context = super().get_context_data(**kwargs)
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        context['entry_pk'] = entry.pk
        context['entry_name'] = entry.entry_name
        context['entry'] = entry
        return context

    def form_valid(self, form):
        """Upon successful upload, the new image will be associated with the entry specified by the URL"""
        self.object = form.save(commit=False)
        self.object.entry = Entry.objects.get(pk=self.kwargs['pk'])
        self.object.save()
        messages.success(self.request, 'Image was successfully uploaded!')
        return super().form_valid(form)


class ImageDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'image_delete.html'
    model = Image

    def test_func(self):
        """Page will only be shown to the entry's author or to users with editor privileges"""
        entry = Entry.objects.get(pk=self.kwargs['pk'])
        is_editor_or_superuser = self.request.user.is_superuser or self.request.user.groups.filter(name='editor').exists()
        return entry.author == self.request.user or is_editor_or_superuser

    def get_success_url(self):
        """Upon successful upload, user will be returned to the image upload page"""
        return reverse_lazy('image_upload', kwargs={'pk': self.object.entry.pk})

    def get_context_data(self, **kwargs):
        """Used for the 'Back' button linking to the entry's image upload page"""
        context = super().get_context_data(**kwargs)
        context['entry'] = self.object.entry
        return context
