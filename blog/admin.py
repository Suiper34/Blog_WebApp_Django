from django.contrib import admin

from .models import Comments, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date')
    search_fields = ('title', 'author__username')
    list_filter = ('date',)


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ('the_user', 'post', 'date')
    search_fields = ('the_user__username', 'post__title')
