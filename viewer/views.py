from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def trips(request):
    return render(request, "trips.html")