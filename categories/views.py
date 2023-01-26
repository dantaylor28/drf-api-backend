from django.shortcuts import render
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics, filters
from drf_api.permissions import IsAdminOrReadOnly


class CategoryListView(generics.ListCreateAPIView):
    """
    A list view of all categories and how many posts are in
    each. Only an admin can create new categories.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        num_of_posts=Count('post', distinct=True)
    )

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = ['name']
    ordering_fields = ['timestamp']


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve a specified category and edit or delete it only if
    you are an admin.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        num_of_posts=Count('post', distinct=True)
    )
