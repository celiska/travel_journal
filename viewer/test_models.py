from django.test import TestCase
from django.contrib.auth.models import User
from .models import Country, Place, Transport, Weather, Hashtag, Entry, Image

class CountryModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(country="Czech Republic", code="CZ")

    def test_country_creation(self):
        self.assertEqual(str(self.country), "Czech Republic")
        self.assertEqual(self.country.code, "CZ")

class PlaceModelTest(TestCase):
    def setUp(self):
        self.country = Country.objects.create(country="Czech Republic", code="CZ")
        self.place = Place.objects.create(place="Prague", country=self.country)

    def test_place_creation(self):
        self.assertEqual(str(self.place), "Prague")
        self.assertEqual(self.place.country, self.country)

class TransportModelTest(TestCase):
    def setUp(self):
        self.transport = Transport.objects.create(type="Car")

    def test_transport_creation(self):
        self.assertEqual(str(self.transport), "Car")

class WeatherModelTest(TestCase):
    def setUp(self):
        self.weather = Weather.objects.create(type="Sunny")

    def test_weather_creation(self):
        self.assertEqual(str(self.weather), "Sunny")

class HashtagModelTest(TestCase):
    def setUp(self):
        self.hashtag = Hashtag.objects.create(hashtag="travel")

    def test_hashtag_creation(self):
        self.assertEqual(str(self.hashtag), "travel")

from datetime import date

class EntryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.country = Country.objects.create(country="Czech Republic", code="CZ")
        self.place = Place.objects.create(place="Prague", country=self.country)
        self.entry = Entry.objects.create(
            entry_name="Trip to Prague",
            author=self.user,
            description="Amazing trip to Prague",
            arrival_date=date(2024, 10, 1),
            departure_date=date(2024, 10, 5),
            cost=1000.00
        )
        self.entry.country.add(self.country)
        self.entry.place.add(self.place)

    def test_entry_creation(self):
        self.assertEqual(str(self.entry), "Trip to Prague")
        self.assertEqual(self.entry.author.username, "testuser")
        self.assertEqual(self.entry.cost, 1000.00)

    def test_duration_calculation(self):
        duration = self.entry.calculate_duration()
        self.assertEqual(duration, 4)


class ImageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.entry = Entry.objects.create(
            entry_name="Trip to Prague",
            author=self.user,
            description="Amazing trip to Prague"
        )
        self.image = Image.objects.create(image="test_image.jpg", entry=self.entry)

    def test_image_creation(self):
        self.assertEqual(str(self.image), "test_image.jpg")
        self.assertEqual(self.image.entry, self.entry)
