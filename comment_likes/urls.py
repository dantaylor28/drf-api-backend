from django.urls import path
from comment_likes import views

urlpatterns = [
    path('comments/likes/', views.CommentLikeListView.as_view()),
    path('comments/likes/<int:pk>', views.CommentLikeDetailView.as_view()),
]
