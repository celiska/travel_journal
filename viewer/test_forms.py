from django.contrib.auth.models import User
from viewer.forms import EntryCreateForm, ImageUploadForm
from viewer.models import Country, Weather, Transport
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from PIL import Image
import io

class EntryCreateFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.country = Country.objects.create(country="Czech Republic", code="CZ")
        self.weather = Weather.objects.create(type="Sunny")
        self.transport = Transport.objects.create(type="Car")

    def test_valid_entry_form(self):
        form_data = {
            'entry_name': 'Trip to Prague',
            'description': 'Amazing trip to Prague',
            'country': [self.country.id],
            'place': 'Prague',
            'places_countries': 'Prague:{};'.format(self.country.id),
            'arrival_date': '2024-10-01',
            'departure_date': '2024-10-05',
            'cost': 1000.00,
            'currency': 'USD',
            'rating': 5,
            'is_private': True,
            'weather': [self.weather.id],
            'transport': [self.transport.id]
        }
        form = EntryCreateForm(data=form_data)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())

    def test_invalid_entry_form_no_place_or_country(self):
        form_data = {
            'entry_name': 'Trip to Prague',
            'description': 'Amazing trip to Prague',
            'arrival_date': '2024-10-01',
            'departure_date': '2024-10-05',
        }
        form = EntryCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('Please add at least one place and country.', form.errors['__all__'])

    def test_invalid_dates(self):
        form_data = {
            'entry_name': 'Trip to Prague',
            'description': 'Amazing trip to Prague',
            'country': [self.country.id],
            'place': 'Prague',
            'arrival_date': '2024-10-05',
            'departure_date': '2024-10-01',
            'cost': 1000.00,
            'currency': 'USD',
            'rating': 5,
        }
        form = EntryCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("The departure date cannot be earlier than the arrival date.", form.errors['__all__'])

    def test_future_arrival_date(self):
        form_data = {
            'entry_name': 'Trip to Prague',
            'description': 'Amazing trip to Prague',
            'country': [self.country.id],
            'place': 'Prague',
            'arrival_date': (date.today().replace(year=date.today().year + 1)).strftime('%Y-%m-%d'),
            'departure_date': '2024-10-05',
            'cost': 1000.00,
            'currency': 'USD',
            'rating': 5,
        }
        form = EntryCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("The arrival date cannot be in the future.", form.errors['__all__'])


class ImageUploadFormTest(TestCase):
    def generate_image(self):
        image = Image.new('RGB', (100, 100), color = 'red')
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        return SimpleUploadedFile("test_image.jpg", byte_arr.read(), content_type="image/jpeg")

    def test_valid_image_form(self):
        img = self.generate_image()
        form_data = {
            'description': 'A beautiful photo from Prague.'
        }
        form_files = {'image': img}
        form = ImageUploadForm(data=form_data, files=form_files)
        if not form.is_valid():
            print("Form errors:", form.errors)
        self.assertTrue(form.is_valid())
