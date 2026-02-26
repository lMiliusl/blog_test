from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'article', 'created_at', 'parent')
    list_filter = ('created_at', 'author')
    search_fields = ('content',)
    readonly_fields = ('content_at', 'updated_at')
