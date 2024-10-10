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
from django.views.generic import TemplateView
from django.urls import path
from django.views.generic import TemplateView

from travel_journal import settings
from accounts.views import SignUpView, user_logout, profile_update, profile_view, delete_user
from viewer.views import home, entry_list, EntryCreateView, EntryDetailView
from viewer import views
from viewer.views import home, EntriesList, entry_list, EntryCreateView, EntryDetailView, search_results, \
    ImageUploadView, ImageDeleteView
from viewer.views import home, EntriesList, entry_list, EntryCreateView, EntryDetailView, EntryUpdateView, \
    EntryDeleteView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', home, name='home'),

    path('entries/', entry_list, name='entries'),
    path('entries/create', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<pk>', EntryDetailView.as_view(), name='entry'),
    path('entry/<pk>/update', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<pk>/delete', EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/<pk>/image_upload', ImageUploadView.as_view(), name='image_upload'),

    path('image_delete/<pk>', ImageDeleteView.as_view(), name='image_delete'),

    path('faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('search/', search_results, name='search_results'),
    path('entries/create', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<pk>', EntryDetailView.as_view(), name='entry'),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/update/', profile_update, name='update_account'),
    path('accounts/profile/<username>', profile_view, name='profile'),
    path('accounts/delete/', delete_user, name='delete_account'),
    path('accounts/', include('django.contrib.auth.urls')),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)