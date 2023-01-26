from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(username='Dan', password='password1')

    def test_list_all_posts(self):
        dan = User.objects.get(username='Dan')
        Post.objects.create(owner=dan, title='test')
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_out_cannot_post(self):
        response = self.client.post('/posts/', {'title': 'test2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_post(self):
        self.client.login(username='Dan', password='password1')
        response = self.client.post('/posts/', {'title': 'test2'})
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
