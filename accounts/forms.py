from django.contrib.auth.forms import UserCreationForm
from django.db.transaction import atomic
from django.forms import CharField, Textarea

from .models import Profile

class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ["username", "password1", "password2"]

    display_name = CharField()
    bio = CharField(widget=Textarea(attrs={"class": "form-control"}),
                    max_length=500,
                    label="Write some info about yourself",
                    required=False)

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

