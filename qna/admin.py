from django.contrib import admin

from .models import Answer, AnswerVote, Question, QuestionVote, Tag


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "answer_count", "vote_count", "created_at")
    list_filter = ("status",)
    filter_horizontal = ("tags",)
    prepopulated_fields = {"slug": ("title",)}


admin.site.register((Answer, Tag, QuestionVote, AnswerVote))
