from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Post

def list_posts(request):
    post_list = Post.published.all()
    paginator = Paginator(post_list, 2)
    page_number = request.GET.get('page', 1)
    posts = paginator.page(page_number)

    return render(request, 'blog/post/list.html', {'posts': posts})


def detail_post(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post, publish__year=year, publish__month=month, publish__day=day, status=Post.Status.PUBLISHED)
    return render(request, 'blog/post/detail.html', {'post': post})
