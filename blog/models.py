from django.conf import settings
from django.db import models
from django.urls import reverse

from common.models import TimestampedModel
from common.utils import unique_slug


class Tag(TimestampedModel):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)


class Post(TimestampedModel):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published")]
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=220)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.CharField(max_length=320)
    body = models.TextField(help_text="Markdown supported")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")
    reading_time = models.PositiveIntegerField(default=4)
    views_count = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("-published_at", "-created_at")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        if self.body:
            self.reading_time = max(1, round(len(self.body.split()) / 200))
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


class Comment(TimestampedModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ("created_at",)
