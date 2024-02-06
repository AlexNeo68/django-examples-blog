from django.shortcuts import get_object_or_404, render

from .models import Post

def list_posts(request):
    posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'posts': posts})


def detail_post(request, id):
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})
