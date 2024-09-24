from django.db import models

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

class City(models.Model):
    city = models.CharField(max_length=100, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name_plural = "Cities"
        ordering = ["city"]

    def __str__(self):
        return self.city

    def __repr__(self):
        return f"City(city={self.city})"

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

class Entry(models.Model):
    entry_name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    country = models.ManyToManyField(Country, blank=False)
    City = models.ManyToManyField(City, blank=False)
    arrival_date = models.DateField(null=False, blank=False)
    departure_date = models.DateField(null=True, blank=True)
    stayed_for = models.IntegerField(null=True, blank=True)
    transport = models.ManyToManyField(Transport, blank=False)
    cost = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    weather = models.ManyToManyField(Weather, blank=False)
    rating = models.IntegerField(default=0, null=False, blank=False)
    hashtag = models.ManyToManyField(Hashtag, blank=True)

    class Meta:
        verbose_name_plural = "Entries"
        ordering = ["arrival_date"]

    def __str__(self):
        return self.entry_name

    def __repr__(self):
        return f"Entry(entry_name={self.entry_name})"

    def calculate_duration(self):
        if self.arrival_date and self.departure_date:
            duration = self.arrival_date - self.departure_date
            return duration.days
