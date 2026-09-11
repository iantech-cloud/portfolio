from django.conf import settings
from django.db import models
from django.urls import reverse

from common.models import TimestampedModel
from common.utils import unique_slug


class Brief(TimestampedModel):
    STATUS_CHOICES = [("open", "Open"), ("in_review", "In review"), ("closed", "Closed")]
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="briefs")
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    budget = models.CharField(max_length=100, blank=True)
    stack = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    selected_solution = models.ForeignKey("Solution", null=True, blank=True, on_delete=models.SET_NULL, related_name="+")
    solution_count = models.PositiveIntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)
    is_student_question = models.BooleanField(default=False)
    math_content = models.TextField(blank=True, help_text="Optional LaTeX-friendly working or formula content.")
    attachment = models.FileField(upload_to="upwork/questions/%Y/%m/", blank=True)
    answer = models.TextField(blank=True)
    answer_preview = models.TextField(blank=True)
    answered_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("upwork:detail", kwargs={"slug": self.slug})


class Solution(TimestampedModel):
    brief = models.ForeignKey(Brief, on_delete=models.CASCADE, related_name="solutions")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="solutions")
    body = models.TextField()
    approach = models.TextField(blank=True)
    vote_count = models.IntegerField(default=0)
    is_selected = models.BooleanField(default=False)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("brief", "author"), name="one_solution_per_author")]


class SolutionVote(TimestampedModel):
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("solution", "user"), name="one_solution_vote")]
