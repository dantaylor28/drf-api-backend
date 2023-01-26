from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import CommentLike
from .serializers import CommentLikeSerializer
from rest_framework import generics
from drf_api.permissions import IsOwnerOrReadOnly


class CommentLikeListView(generics.ListCreateAPIView):
    """
    A list of all comment likes with fields that show the liked
    comment, which user liked it and its timestamp. Can be filtered
    by different comments.
    """
    serializer_class = CommentLikeSerializer
    queryset = CommentLike.objects.all().order_by('-timestamp')

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['comment']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentLikeDetailView(generics.RetrieveDestroyAPIView):
    """
    Retrieve a single liked comment. The ability to delete a like
    is available if you are the owner of it.
    """
    serializer_class = CommentLikeSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = CommentLike.objects.all()
