from django.contrib import admin

from .models import Category, GalleryImage, Project, Tag


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "status", "featured", "views_count")
    list_filter = ("status", "featured", "category")
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((Category, Tag, GalleryImage))
