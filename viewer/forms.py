from datetime import date
from django import forms
from django.core.exceptions import ValidationError
from viewer.models import Entry, Country, Weather, Transport, CURRENCY_CHOICES, Place, Hashtag, RATING_CHOICES, Image


class EntryCreateForm(forms.ModelForm):
    class Meta:
        model = Entry
        exclude = ['author']

    is_private = forms.ChoiceField(
        choices=[(True, 'Private'), (False, 'Public')],
        widget=forms.RadioSelect,
        initial=True
    )

    entry_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control ', 'maxlength': '50'})
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'maxlength': '1200'})
    )

    country = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )

    place = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )

    weather = forms.ModelMultipleChoiceField(
        queryset=Weather.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    transport = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False
    )

    arrival_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=False
    )

    cost = forms.DecimalField(
        min_value=0,
        decimal_places=2,  # Oprava: decimal_places pro přesnost
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    hashtags = forms.CharField(
        max_length=50,
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['weather', 'transport']:
            self.fields[field].label_from_instance = lambda obj: obj.type.replace('_', ' ').capitalize()

    def save(self, commit=True):
        entry = super().save(commit=False)

        if commit:
            entry.save()

        places_countries_data = self.data.get('places_countries', '')

        if places_countries_data:
            places_countries_list = places_countries_data.split(';')

            for item in places_countries_list:
                if item:
                    place_name, country_id = item.split(':')
                    country = Country.objects.get(id=country_id)
                    place, created = Place.objects.get_or_create(place=place_name.strip(), country=country)
                    entry.place.add(place)
                    entry.country.add(country)

        place_name = self.cleaned_data.get('place', '').strip()
        countries = self.cleaned_data.get('country', None)

        if place_name and countries:
            for country in countries:
                place, created = Place.objects.get_or_create(place=place_name, country=country)
                entry.place.add(place)

        hashtags_str = self.cleaned_data.get('hashtags', '')
        if hashtags_str:
            hashtags = [Hashtag.objects.get_or_create(hashtag=tag.strip())[0] for tag in hashtags_str.split(',') if
                        tag.strip()]
            entry.hashtag.set(hashtags)

        entry.weather.set(self.cleaned_data.get('weather', []))
        entry.transport.set(self.cleaned_data.get('transport', []))

        return entry

    def clean(self):
        cleaned_data = super().clean()
        places_countries_data = self.data.get('places_countries', '').strip()
        arrival_date = cleaned_data.get("arrival_date")
        departure_date = cleaned_data.get("departure_date")

        if not self.instance.pk and not places_countries_data:
            raise ValidationError("Please add at least one place and country.")

        places_countries_list = places_countries_data.split(';')
        places_countries_list = [item for item in places_countries_list if item]

        cleaned_data['places_countries'] = places_countries_list

        if arrival_date and departure_date:
            if departure_date < arrival_date:
                raise forms.ValidationError("The departure date cannot be earlier than the arrival date.")
        if arrival_date and arrival_date > date.today():
            raise forms.ValidationError("The arrival date cannot be in the future.")
        if departure_date and departure_date > date.today():
            raise forms.ValidationError("The departure date cannot be in the future.")

        return cleaned_data


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'description']

    image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'}),
        required=True,
    )

    description = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=False
    )
