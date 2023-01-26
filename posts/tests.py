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


class PostDetailViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')
        Post.objects.create(owner=dan, title='dans post')
        Post.objects.create(owner=sabina, title='sabinas post')

    def test_get_post_by_id(self):
        response = self.client.get('/posts/1')
        self.assertEqual(response.data['title'], 'dans post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existant_id(self):
        response = self.client.get('posts/32')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_post(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/posts/1', {'title': 'dans updated post'})
        post = Post.objects.filter(pk=1).first()
        self.assertEqual(post.title, 'dans updated post')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_others_post(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/posts/2', {'title': 'dans post now'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
