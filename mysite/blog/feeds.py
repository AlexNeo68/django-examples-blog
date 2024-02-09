
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from markdown import markdown

from .models import Post
class LatestPostFeed(Feed):
    title = 'Latest posts in the blog'
    link = reverse_lazy('blog:post-list')
    description = 'My post in my blog'

    def items(self):
        return Post.published.order_by('-publish')[:5]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords_html(markdown(item.body), 30)
    
    def item_pubdate(self, item):
        return item.publish