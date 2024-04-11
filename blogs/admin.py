from django.contrib import admin
from .models import Blog, Like, Comment


class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'is_published', 'scheduled_date')


admin.site.register(Blog, BlogAdmin)


class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'created_at',)


admin.site.register(Like, LikeAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'blog', 'created_at',)


admin.site.register(Comment, CommentAdmin)
