from django.urls import path
from .views import PostDetails, PostCreateView, PostDeleteView

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetails.as_view(), name='post_details'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
]
