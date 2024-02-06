from django.urls import path

from .views import detail_post, list_posts


app_name = 'blog'

urlpatterns = [
    path('', list_posts, name='post-list'),
    path('<int:id>/', detail_post, name='post-detail')
]
