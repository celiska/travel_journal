from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from viewer.models import Entry, Country


class HomeViewTest(TestCase):
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


class EntryCreateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.country = Country.objects.create(country='Czech Republic', code='CZ')

    def test_create_entry_view_get(self):
        response = self.client.get(reverse('entry_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry_form.html')

    def test_create_entry_view_post(self):
        form_data = {
            'entry_name': 'Test Entry',
            'description': 'Description of test entry',
            'arrival_date': '2024-01-01',
            'departure_date': '2024-01-05',
            'cost': 1000.00,
            'currency': 'USD',
            'rating': 5,
            'is_private': True,
            'places_countries': 'Prague:{};'.format(self.country.id),
        }
        response = self.client.post(reverse('entry_create'), data=form_data)
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)


class EntryUpdateViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.entry = Entry.objects.create(
            entry_name='Test Entry',
            description='Test description',
            author=self.user
        )
        self.client.login(username='testuser', password='12345')

    def test_update_entry_view_get(self):
        response = self.client.get(reverse('entry_update', kwargs={'pk': self.entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry_form.html')

    def test_update_entry_view_post(self):
        form_data = {
            'entry_name': 'Updated Entry',
            'description': 'Updated description',
            'rating': 5,
            'is_private': True,
        }
        response = self.client.post(reverse('entry_update', kwargs={'pk': self.entry.pk}), data=form_data)
        if response.status_code != 302:
            print("Form errors:", response.context['form'].errors)
        self.assertEqual(response.status_code, 302)


class EntryDeleteViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.entry = Entry.objects.create(
            entry_name='Test Entry',
            description='Test description',
            author=self.user
        )
        self.client.login(username='testuser', password='12345')

    def test_delete_entry_view_post(self):
        response = self.client.post(reverse('entry_delete', kwargs={'pk': self.entry.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Entry.objects.filter(pk=self.entry.pk).exists())


class EntryDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.entry = Entry.objects.create(
            entry_name='Test Entry',
            description='Test description',
            author=self.user
        )

    def test_entry_detail_view(self):
        response = self.client.get(reverse('entry_detail', kwargs={'pk': self.entry.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entry_detail.html')
        self.assertContains(response, 'Test Entry')
