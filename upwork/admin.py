from django.contrib import admin

from .models import Brief, Solution, SolutionVote


@admin.register(Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "status", "is_student_question", "answered_at", "created_at")
    list_filter = ("status", "is_student_question")
    search_fields = ("title", "description", "client__username")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (("Question", {"fields": ("client", "title", "slug", "description", "math_content", "attachment", "is_student_question", "status")}), ("Official answer", {"fields": ("answer_preview", "answer", "answer_unlocked", "answered_at")}))


admin.site.register((Solution, SolutionVote))
