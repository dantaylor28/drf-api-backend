from django.db import models


class Category(models.Model):
    """
    Category model will store different category names in the
    database. A category field is added to the Post model via a
    foreign key to allow posts to be assigned a category upon creation
    """
    name = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
