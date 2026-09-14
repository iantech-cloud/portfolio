from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class NotificationPreference(TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notification_preferences")
    email_comments = models.BooleanField(default=True)
    email_newsletter = models.BooleanField(default=True)
    email_product_updates = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification preferences for {self.user}"


class Notification(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=180)
    body = models.TextField(blank=True)
    url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
