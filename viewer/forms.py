from django import forms
from viewer.models import Entry, Country, Weather, Transport, CURRENCY_CHOICES, Place, Hashtag, RATING_CHOICES


class EntryCreateForm(forms.ModelForm):
    hashtags = forms.CharField(
        max_length=255,
        required=False,
    )

    class Meta:
        model = Entry
        fields = ['entry_name', 'description', 'country', 'place', 'weather', 'transport',
                  'arrival_date', 'departure_date', 'currency', 'rating', 'cost']

    entry_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        label="Název"
    )

    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=True,
        label="Popis"
    )

    country = forms.ModelMultipleChoiceField(
        queryset=Country.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=True,
        label="Země"
    )

    place = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True,
    )

    weather = forms.ModelMultipleChoiceField(
        queryset=Weather.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Počasí"
    )

    transport = forms.ModelMultipleChoiceField(
        queryset=Transport.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        label="Doprava"
    )

    arrival_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    departure_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    cost = forms.DecimalField(
        min_value=0,
        step_size=0.01,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
    )

    currency = forms.ChoiceField(
        choices=CURRENCY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['weather', 'transport']:
            self.fields[field].label_from_instance = lambda obj: obj.type.replace('_', ' ').capitalize()

    def save(self, commit=True):
        entry = super().save(commit=False)

        if commit:
            entry.save()

        countries = self.cleaned_data['country']
        entry.country.set(countries)

        place_name = self.cleaned_data['place'].strip()
        for country in countries:
            place, created = Place.objects.get_or_create(place=place_name, country=country)
            entry.place.add(place)

        hashtags_str = self.cleaned_data.get('hashtags', '')
        if hashtags_str:
            hashtags = [Hashtag.objects.get_or_create(hashtag=tag.strip())[0] for tag in hashtags_str.split(',') if
                        tag.strip()]
            entry.hashtag.add(*hashtags)

        entry.weather.set(self.cleaned_data['weather'])
        entry.transport.set(self.cleaned_data['transport'])

        return entry

    def clean(self):
        cleaned_data = super().clean()
        cost = cleaned_data.get("cost")
        currency = cleaned_data.get("currency")

        if cost and not currency:
            raise forms.ValidationError("Pokud je vyplněná cena, je potřeba vybrat také měnu.")

        return cleaned_data
