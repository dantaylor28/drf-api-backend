from django.urls import path
from pins import views

urlpatterns = [
    path('pins/', views.PinListView.as_view()),
    path('pins/<int:pk>', views.PinDetailView.as_view()),
]
