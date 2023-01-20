from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    The profile model, of which the owner is a instance of the User model.
    A default image is set in case a user does not set one themselves.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    profile_image = models.ImageField(
        upload_to='images/', default='../default_profile_ohvixx'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile | last updated: {self.updated_at}"
