from django.contrib import admin

from viewer.models import Country, Place, Image, Transport, Weather, Entry, Hashtag

# Register your models here.

admin.site.register(Place)
admin.site.register(Country)
admin.site.register(Image)
admin.site.register(Transport)
admin.site.register(Weather)
admin.site.register(Entry)
admin.site.register(Hashtag)