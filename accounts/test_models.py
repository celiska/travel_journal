from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')

    def test_create_profile(self):
        profile = Profile.objects.create(user=self.user, display_name='Test Name')
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.display_name, 'Test Name')

    def test_str_method(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), 'testuser')

    def test_profile_update(self):
        profile = Profile.objects.create(user=self.user, display_name='Old Name')
        profile.display_name = 'New Name'
        profile.save()
        self.assertEqual(Profile.objects.get(user=self.user).display_name, 'New Name')

