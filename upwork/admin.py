from django.contrib import admin

from .models import Brief, Solution, SolutionVote


@admin.register(Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "solution_count", "created_at")
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((Solution, SolutionVote))
