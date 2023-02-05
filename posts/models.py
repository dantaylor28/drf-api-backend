from django.db import models
from django.contrib.auth.models import User
from categories.models import Category


class Post(models.Model):
    """
    The Post model which contains all relevant fields for any posts created.
    A default image is attached in the case of a user not uploading one
    themselves.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, null=True, blank=True)
    post_image = models.ImageField(
        upload_to='images/', default='../default_post_l03unw', blank=True
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} | owner: {self.owner}"
