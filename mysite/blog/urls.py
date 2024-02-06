from django.urls import path

from .views import PostListView, detail_post, list_posts, share_post


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', detail_post, name='post-detail'),
    path('<int:post_id>/share/', share_post, name='post-share'),
]
