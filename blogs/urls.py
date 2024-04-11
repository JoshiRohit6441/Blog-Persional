from django.urls import path
from .views import BlogView, GetblogsView, LikeGeneralView, LikeView,CommentView,CommentGeneralView

urlpatterns = [
    path('blogs/', BlogView.as_view(), name='blog-list'),
    path('blogs/<int:id>/', BlogView.as_view(), name='blog-detail'),
    path('blogs-published/', GetblogsView.as_view(), name='blog-published'),
    path('blogs-published-id/<int:id>/', GetblogsView.as_view(), name='blog-published-id'),
    path('like-get/', LikeGeneralView.as_view(), name='like-get'),
    path('like/', LikeView.as_view(), name='like'),
    path('like-delete/<int:id>/', LikeView.as_view(), name='like-delete'),
    path('comment-get/', CommentGeneralView.as_view(), name='comment-get'),
    path('comment/', CommentView.as_view(), name='comment'),
    path('comment-delete/<int:id>/', CommentView.as_view(), name='comment-delete'),
]
