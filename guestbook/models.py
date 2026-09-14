from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class GuestbookEntry(TimestampedModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="guestbook_entries")
    message = models.TextField(max_length=600)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)


class Book(TimestampedModel):
    title = models.CharField(max_length=220)
    author = models.CharField(max_length=160)
    cover_url = models.URLField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class ReadingItem(TimestampedModel):
    STATUS_CHOICES = [("want", "Want to read"), ("reading", "Reading"), ("finished", "Finished")]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_items")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="readers")
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="want")
    rating = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "book"), name="unique_user_book")]


class NowUpdate(TimestampedModel):
    title = models.CharField(max_length=180)
    body = models.TextField()
    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)


class UsesItem(TimestampedModel):
    category = models.CharField(max_length=120)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("sort_order", "name")


class SpeakingEvent(TimestampedModel):
    title = models.CharField(max_length=220)
    event_name = models.CharField(max_length=180)
    event_date = models.DateField()
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)

    class Meta:
        ordering = ("-event_date",)


class SavedFavorite(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_favorites")
    project = models.ForeignKey("projects.Project", null=True, blank=True, on_delete=models.CASCADE, related_name="saved_by")
    blog_post = models.ForeignKey("blog.Post", null=True, blank=True, on_delete=models.CASCADE, related_name="saved_by")

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "project", "blog_post"), name="unique_saved_favorite")]


class ReadingHistory(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reading_history")
    blog_post = models.ForeignKey("blog.Post", on_delete=models.CASCADE, related_name="reading_history")
    last_read_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("user", "blog_post"), name="unique_reading_history")]
