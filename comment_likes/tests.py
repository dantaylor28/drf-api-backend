from django.contrib.auth.models import User
from .models import CommentLike, Comment
from posts.models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class CommentLikeListViewTests(APITestCase):
    def setUp(self):
        dan = User.objects.create_user(username='dan', password='password1')

    def test_list_all_comment_likes(self):
        dan = User.objects.get(username='dan')
        post1 = Post.objects.create(owner=dan, title='dans post')
        comment1 = Comment.objects.create(owner=dan, post=post1)
        CommentLike.objects.create(owner=dan, comment=comment1)
        response = self.client.get('/comments/likes/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
