from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class SiteSettings(TimestampedModel):
    site_name = models.CharField(max_length=120, default="IANO / systems portfolio")
    role = models.CharField(max_length=180, default="Python engineer, ML builder, systems thinker")
    hero_text = models.TextField(default="I turn hard technical problems into calm, useful software.")
    about_text = models.TextField(default="I build reliable products at the intersection of Python, machine learning, and thoughtful systems design.")
    location = models.CharField(max_length=120, default="Nairobi, Kenya")
    email = models.EmailField(default="hello@example.com")
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.pk = 1
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.site_name


class ContactMessage(TimestampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)


class FAQItem(TimestampedModel):
    question = models.CharField(max_length=240)
    answer = models.TextField()
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "question")


class AuditLog(TimestampedModel):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=120)
    object_type = models.CharField(max_length=120, blank=True)
    object_id = models.CharField(max_length=120, blank=True)
    metadata = models.JSONField(default=dict, blank=True)


class Notification(TimestampedModel):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=220)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=255, blank=True)
