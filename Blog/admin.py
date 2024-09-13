from django.contrib import admin
from .models import Blog_Post, Comment

@admin.register(Blog_Post)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_on_date', 'display_comments')
    list_filter = ('author', 'created_on_date')
    search_fields = ('title', 'author')

    def display_comments(self, obj):
        return ", ".join([comment.message for comment in obj.comments.all()])

    display_comments.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'message', 'display_blog_post_ids')  
    search_fields = ('name', 'email', 'message')

    def display_blog_post_ids(self, obj):
        return ", ".join([str(blog_post.id) for blog_post in obj.blog_posts.all()])

    display_blog_post_ids.short_description = 'Related Blog Post IDs'