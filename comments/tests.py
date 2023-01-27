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

    def test_logged_out_cannot_comment(self):
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        response = self.client.post('/comments/', {'post': 'post1'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_comment(self):
        self.client.login(username='dan', password='password1')
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        response = self.client.post('/posts/', {'text': 'hey'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
