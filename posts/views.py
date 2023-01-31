from django.shortcuts import render
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .serializers import PostSerializer
from drf_api.permissions import IsOwnerOrReadOnly
from rest_framework import generics, filters


class PostListView(generics.ListCreateAPIView):
    """
    Lists out all posts and the ability to create your own
    if you are signed in and authenticated. Posts can be
    filtered, searched and ordered by numerous options.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        num_of_pins=Count('pins', distinct=True),
        num_of_comments=Count('comment', distinct=True)
    ).order_by('-uploaded_at')

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend
    ]

    search_fields = [
        'title',
        'category__name',
        'owner__username',
        'owner__profile__name'
    ]

    ordering_fields = [
        'num_of_pins',
        'num_of_comments'
    ]

    filterset_fields = [
        'owner__profile',
        'category__name',
        # will show posts from users the selected user is following
        'owner__followed__owner__profile',
        # will show posts the selected user has pinned
        'pins__owner__profile'
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Lists a selected post with the ability to edit or delete it
    if you are the post owner
    """
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        num_of_pins=Count('pins', distinct=True),
        num_of_comments=Count('comment', distinct=True)
    ).order_by('-uploaded_at')
