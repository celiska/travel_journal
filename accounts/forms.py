from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.transaction import atomic
from django.forms import CharField, Textarea, ModelForm, TextInput, PasswordInput

from .models import Profile

class SignUpForm(UserCreationForm):
    display_name = CharField(
        max_length=20,
        label="Display name",
        widget=TextInput(attrs={'class': 'form-control'})
    )
    bio = CharField(
        widget=Textarea(attrs={"class": "form-control"}),
        max_length=500,
        label="Write some info about yourself",
        required=False
    )

    class Meta(UserCreationForm.Meta):
        fields = ["username", "password1", "password2"]
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        user = super().save(commit)
        display_name = self.cleaned_data["display_name"]
        bio = self.cleaned_data["bio"]
        profile = Profile(user=user, display_name=display_name, bio=bio)

        if commit:
            profile.save()
        return user

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["username"]

    username = CharField(max_length=150, required=True)

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = ["display_name", "bio", "profile_picture"]

    display_name = CharField(max_length=20)
    bio = CharField(widget=Textarea(attrs={"class": "form-control"}),
                    max_length=500,
                    label="Write some info about yourself",
                    required=False)

