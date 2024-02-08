from django.urls import path

from .views import PostListView, detail_post, list_posts, post_comment, share_post


app_name = 'blog'

urlpatterns = [
    # path('', PostListView.as_view(), name='post-list'),
    path('', list_posts, name='post-list'),
    path('tag/<slug:tag_slug>/', list_posts, name='post-list-by-tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', detail_post, name='post-detail'),
    path('<int:post_id>/share/', share_post, name='post-share'), 
    path('<int:post_id>/comment/', post_comment, name='post-comment'),
]
