from django.db import models, IntegrityError
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import pre_save


class Follower(models.Model):
    """
    The Follower model, with 2 fields with a foreign key to
    User. It uses the related name feature so django can determine
    the different User instances. Stores data relating to Users who
    follow each other.
    """
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followed')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        unique_together = ['owner', 'followed']

    def __str__(self):
        return f"{self.followed} followed by {self.owner}"


# Handles self following attempts and raises IntegrityError if attempted
@receiver(pre_save, sender=Follower)
def stop_self_follow(sender, instance, **kwargs):
    if instance.owner == instance.followed:
        raise IntegrityError()
