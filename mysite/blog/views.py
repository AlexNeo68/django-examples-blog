from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView
from django.views.decorators.http import require_POST
from django.contrib.postgres.search import TrigramSimilarity, SearchVector, SearchQuery, SearchRank

from .forms import CommentForm, EmailPostForm, SearchForm

from .models import Comment, Post
from taggit.models import Tag

from django.db.models import Count


@require_POST
def post_comment(request: HttpRequest, post_id: int):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    form = CommentForm(data=request.POST)
    comment = None
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        "post": post,
        "form": form,
        "comment": comment,
    }

    return render(request, "blog/post/comment.html", context)


def list_posts(request, tag_slug=None):


    post_list = Post.published.all()

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])

    paginator = Paginator(post_list, 2)
    page_number = request.GET.get("page", 1)

    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "blog/post/list.html", {"posts": posts, "tag": tag})


def detail_post(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        status=Post.Status.PUBLISHED,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()

    post_tags_id = post.tags.values_list('id', flat=True)
    semilar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    semilar_posts = semilar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    context = {
        "post": post,
        "form": form,
        "comments": comments,
        "semilar_posts": semilar_posts,
    }
    return render(request, "blog/post/detail.html", context)


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 2
    template_name = "blog/post/list.html"


def share_post(request: HttpRequest, post_id):
    post = get_object_or_404(Post, id=post_id)

    sent = False

    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            post_url = request.build_absolute_uri(post.get_absolute_url())

            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )

            send_mail(subject, message, "", [cd["to"]])

            sent = True
    else:
        form = EmailPostForm()

    return render(
        request, "blog/post/share.html", {"post": post, "form": form, "sent": sent}
    )

def post_search(request: HttpRequest):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        # if form.is_valid():
        #     query = form.cleaned_data['query']
        #     # search_vector = SearchVector('title', 'body', config="spanish")
        #     search_vector = SearchVector('title', weight="A") + \
        #         SearchVector('body', weight="B")
        #     search_query = SearchQuery(query)
        #     results = Post.published.annotate(
        #         search=search_vector, 
        #         rank = SearchRank(search_vector, search_query)
        #     ).filter(
        #         # search=search_query
        #         rank__gte=0.3
        #     ).order_by('-rank')

        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(
                similarity=TrigramSimilarity('title', query), 
            ).filter(
                similarity__gt=0.1
            ).order_by('-similarity')

    context = {
        'form': form,
        'query': query,
        'results': results,
    }

    return render(request, 'blog/post/search.html', context)
