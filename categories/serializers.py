from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Category serializer. Num_of_posts uses count to list the
    number of posts in each category.
    """
    num_of_posts = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'timestamp', 'num_of_posts'
        ]
