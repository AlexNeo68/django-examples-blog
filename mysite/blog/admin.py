from django.contrib import admin

from .models import Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = 'title', 'slug', 'author', 'status', 'publish'
    list_filter = 'publish', 'created', 'status', 'author'
    search_fields = 'title', 'body'
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    save_as= True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = 'name', 'email', 'post', 'created', 'active'
    list_filter = 'created', 'updated', 'active'
    search_fields = 'name', 'body'