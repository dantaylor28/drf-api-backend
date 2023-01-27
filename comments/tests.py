from django.contrib.auth.models import User
from .models import Comment, Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentListViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')

    def test_list_all_comments(self):
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        Comment.objects.create(owner=dan, post=post1)
        response = self.client.get('/comments/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
