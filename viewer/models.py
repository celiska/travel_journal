from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey


# Create your models here.
class Country(models.Model):
    country = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["code"]

    def __str__(self):
        return self.country

    def __repr__(self):
        return f"Country(country={self.country}, code={self.code})"

class Place(models.Model):
    place = models.CharField(max_length=100, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Places"
        ordering = ["place"]

    def __str__(self):
        return self.place

    def __repr__(self):
        return f"Place(place={self.place})"

class Transport(models.Model):
    type = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["type"]

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"Transport(type={self.type})"

class Weather(models.Model):
    type = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        ordering = ["type"]

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"Weather(type={self.type})"

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Hashtags"
        ordering = ["hashtag"]

    def __str__(self):
        return self.hashtag

    def __repr__(self):
        return f"Hashtag(hashtag={self.hashtag})"

CURRENCY_CHOICES = (
    ("AUD", "Australian dollar (AUD)"),
    ("CNY", "Chinese yuan (CNY)"),
    ("CZK", "Czech koruna (CZK)"),
    ("EUR", "Euro (EUR)"),
    ("GBP", "Pound sterling (GBP)"),
    ("USD", "U.S. dollar (USD)")
)

RATING_CHOICES = (
    (1, "⭐"),
    (2, "⭐⭐"),
    (3, "⭐⭐⭐"),
    (4, "⭐⭐⭐⭐"),
    (5, "⭐⭐⭐⭐⭐")
)

class Entry(models.Model):
    entry_name = models.CharField(max_length=100, null=False, blank=False)
    author = ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    country = models.ManyToManyField(Country, blank=False)
    place = models.ManyToManyField(Place, blank=False)
    arrival_date = models.DateField(null=True, blank=True)
    departure_date = models.DateField(null=True, blank=True)
    stayed_for = models.IntegerField(null=True, blank=True)
    transport = models.ManyToManyField(Transport, blank=True)
    cost = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default="USD", null=True, blank=True)
    weather = models.ManyToManyField(Weather, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, default=1, null=True, blank=True)
    hashtag = models.ManyToManyField(Hashtag, blank=True)
    is_private = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ["arrival_date"]

    def __str__(self):
        return self.entry_name

    def __repr__(self):
        return f"Entry(entry_name={self.entry_name})"

    def calculate_duration(self):
        if self.arrival_date and self.departure_date:
            duration = self.departure_date - self.arrival_date
            return duration.days

class Image(models.Model):
    image = models.ImageField(null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.image.name

    def __repr__(self):
        return f"Image(image={self.image})"
