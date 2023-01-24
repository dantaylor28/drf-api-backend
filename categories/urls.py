from django.urls import path
from categories import views

urlpatterns = [
    path('categories/', views.CategoryListView.as_view()),
    path('categories/<int:pk>', views.CategoryDetailView.as_view()),
]
