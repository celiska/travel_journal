from django.db import models

# Create your models here.
class Entry(models.Model):
    entry_name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    arrival_date = models.DateField(null=False, blank=False)
    departure_date = models.DateField(null=True, blank=True)
    # stayed_for
    cost = models.DecimalField(max_digits=7, decimal_places=2)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.entry_name

    def __repr__(self):
        return f"Entry(entry_name={self.entry_name})"

class Country(models.Model):
    country = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=3, null=False, blank=False)

    def __str__(self):
        return self.country

    def __repr__(self):
        return f"Country(country={self.country})"

class Hashtag(models.Model):
    hashtag = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.hashtag

    def __repr__(self):
        return f"Hashtag(hashtag={self.hashtag})"

class City(models.Model):
    city = models.CharField(max_length=100, null=False, blank=False)

class Transport(models.Model):
    pass

class Weather(models.Model):
    pass
