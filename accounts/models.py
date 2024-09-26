from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    bio = models.TextField()

    class Meta:
        ordering = ['user__username']

    def __str__(self):
        return f"{self.user}"

    def __repr__(self):
        return f"Profile(user={self.user})"
