from django.shortcuts import render
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics
from drf_api.permissions import IsOwnerOrReadOnly, IsAdminOrReadOnly


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    queryset = Category.objects.all()
