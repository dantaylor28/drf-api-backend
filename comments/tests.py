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


class CommentDetailViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')
        sabina = User.objects.create_user(
            username='sabina', password='password1')
        post1 = Post.objects.create(owner=dan, title='dans post')
        post2 = Post.objects.create(owner=sabina, title='sabinas post')
        Comment.objects.create(owner=dan, post=post2, text='hi')
        Comment.objects.create(owner=sabina, post=post1, text='bye')

    def test_get_comment_by_id(self):
        response = self.client.get('/comments/1')
        self.assertEqual(response.data['text'], 'hi')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existant_comment_id(self):
        response = self.client.get('comments/32')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_own_comment(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/comments/1', {'text': 'new comment'})
        comment = Comment.objects.filter(pk=1).first()
        self.assertEqual(comment.text, 'new comment')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_others_comment(self):
        self.client.login(username='dan', password='password1')
        response = self.client.put('/comments/2', {'text': 'new comment'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
