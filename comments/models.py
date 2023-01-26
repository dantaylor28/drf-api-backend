from django.db import models
from django.contrib.auth.models import User
from posts.models import Post


class Comment(models.Model):
    """
    The Comment model, which holds information on the comment text,
    the user who made it and the relevant timestamp and updated_at
    fields. Foreign key to the User and Post model.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.owner} | commented: {self.text}"
