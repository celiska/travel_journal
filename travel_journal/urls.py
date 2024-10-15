from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from travel_journal import settings
from accounts.views import SignUpView, user_logout, profile_update, delete_user, profile_view
from viewer.views import home, entry_list, EntryCreateView, EntryDetailView, EntryUpdateView, \
    EntryDeleteView, search_results, ImageUploadView, ImageDeleteView, EntriesEditView

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    path('', home, name='home'),

    path('entries/', entry_list, name='entries'),
    path('entries/create', EntryCreateView.as_view(), name='entry_create'),
    path('entry/<pk>', EntryDetailView.as_view(), name='entry'),
    path('entry/<pk>/update', EntryUpdateView.as_view(), name='entry_update'),
    path('entry/<pk>/delete', EntryDeleteView.as_view(), name='entry_delete'),
    path('entry/<pk>/image_upload', ImageUploadView.as_view(), name='image_upload'),
    path('entries_edit', EntriesEditView.as_view(), name='edit_panel'),

    path('image_delete/<pk>', ImageDeleteView.as_view(), name='image_delete'),

    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', user_logout, name='logout'),
    path('accounts/update/', profile_update, name='profile_update'),
    path('accounts/profile/<username>', profile_view, name='profile'),
    path('accounts/delete/', delete_user, name='delete_account'),
    path('accounts/', include('django.contrib.auth.urls')),

    path('faq', TemplateView.as_view(template_name='faq.html'), name='faq'),
    path('contact', TemplateView.as_view(template_name='contact.html'), name='contact'),

    path('search/', search_results, name='search_results'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
