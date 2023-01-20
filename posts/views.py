from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
from rest_framework import generics


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().order_by('-uploaded_at')


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
