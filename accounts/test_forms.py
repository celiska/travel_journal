from django.test import TestCase
from django.contrib.auth.models import User
from accounts.forms import SignUpForm, UserUpdateForm, ProfileUpdateForm
from accounts.models import Profile

class FormsTest(TestCase):
    def test_signup_form(self):
        form_data = {
            'username': 'newuser',
            'password1': 'strongpassword123',
            'password2': 'strongpassword123',
            'display_name': 'New User',
            'bio': 'This is a test bio.'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertTrue(Profile.objects.filter(user=user, display_name='New User').exists())

    def test_user_update_form(self):
        user = User.objects.create(username='testuser')
        form_data = {'username': 'updateduser'}
        form = UserUpdateForm(instance=user, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        user.refresh_from_db()
        self.assertEqual(user.username, 'updateduser')

    def test_profile_update_form(self):
        user = User.objects.create(username='testuser')
        profile = Profile.objects.create(user=user, display_name='Old Name')
        form_data = {'display_name': 'Updated Name', 'bio': 'Updated bio'}
        form = ProfileUpdateForm(instance=profile, data=form_data)
        self.assertTrue(form.is_valid())
        form.save()
        profile.refresh_from_db()
        self.assertEqual(profile.display_name, 'Updated Name')
        self.assertEqual(profile.bio, 'Updated bio')
