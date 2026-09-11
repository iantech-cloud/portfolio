from django.conf import settings
from django.db import models
from django.urls import reverse

from common.models import TimestampedModel
from common.utils import unique_slug


class Tag(TimestampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)


class Question(TimestampedModel):
    STATUS_CHOICES = [("draft", "Draft"), ("open", "Open"), ("answered", "Answered"), ("closed", "Closed")]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    tags = models.ManyToManyField(Tag, blank=True, related_name="questions")
    answer_count = models.PositiveIntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("qna:detail", kwargs={"slug": self.slug})


class Answer(TimestampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="answers")
    body = models.TextField()
    vote_count = models.IntegerField(default=0)
    is_accepted = models.BooleanField(default=False)


class QuestionVote(TimestampedModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("question", "user"), name="one_question_vote")]


class AnswerVote(TimestampedModel):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("answer", "user"), name="one_answer_vote")]
