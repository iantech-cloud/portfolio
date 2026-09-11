from django.contrib import admin

from .models import Comment, Post, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "published_at", "views_count")
    list_filter = ("status",)
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((Tag, Comment))
