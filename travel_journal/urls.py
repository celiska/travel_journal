"""
URL configuration for travel_journal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from travel_journal import settings
from accounts.views import SignUpView, user_logout, profile_update, profile_view
from viewer import views
from viewer.views import home, EntriesList, entry_list, EntryCreateView, EntryDetailView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', home, name='home'),

    path('entries/', entry_list, name='entries'),
    path('entries/create', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<pk>', EntryDetailView.as_view(), name='entry'),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/update/', profile_update, name='update'),
    path('accounts/profile/<username>', profile_view, name='profile'),
    path('accounts/', include('django.contrib.auth.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
