from django.shortcuts import render
from django.db.models import Count
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics
from drf_api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        num_of_posts=Count('post', distinct=True)
    )


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.annotate(
        num_of_posts=Count('post', distinct=True)
    )
