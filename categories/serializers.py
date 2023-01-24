from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    num_of_posts = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'timestamp', 'num_of_posts'
        ]
