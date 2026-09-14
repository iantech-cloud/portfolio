import secrets
from django.db import models
from django.utils import timezone
from common.models import TimestampedModel


class NewsletterSubscriber(TimestampedModel):
    STATUS_CHOICES = [
        ("pending", "Pending Confirmation"),
        ("confirmed", "Confirmed"),
        ("unsubscribed", "Unsubscribed"),
    ]
    email = models.EmailField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    confirmation_token = models.CharField(max_length=64, unique=True, blank=True)
    unsubscribe_token = models.CharField(max_length=64, unique=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    bounce_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "-created_at"]),
            models.Index(fields=["confirmation_token"]),
            models.Index(fields=["unsubscribe_token"]),
        ]

    def __str__(self):
        return f"{self.email} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.confirmation_token:
            self.confirmation_token = secrets.token_urlsafe(48)
        if not self.unsubscribe_token:
            self.unsubscribe_token = secrets.token_urlsafe(48)
        super().save(*args, **kwargs)

    def confirm(self):
        self.status = "confirmed"
        self.confirmed_at = timezone.now()
        self.save()

    def unsubscribe(self):
        self.status = "unsubscribed"
        self.unsubscribed_at = timezone.now()
        self.save()


class NewsletterCampaign(TimestampedModel):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("scheduled", "Scheduled"),
        ("sending", "Sending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    ]
    title = models.CharField(max_length=220)
    subject = models.CharField(max_length=220)
    html_body = models.TextField()
    text_body = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    sent_count = models.PositiveIntegerField(default=0)
    failed_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(fields=["status", "-scheduled_at"]),
        ]

    def __str__(self):
        return f"{self.title} ({self.status})"
