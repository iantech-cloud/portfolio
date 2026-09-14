from django.contrib import admin
from .models import NewsletterSubscriber, NewsletterCampaign


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "status", "confirmed_at", "created_at")
    list_filter = ("status", "created_at", "confirmed_at")
    search_fields = ("email",)
    readonly_fields = ("confirmation_token", "unsubscribe_token", "created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "status")}),
        ("Tokens", {"fields": ("confirmation_token", "unsubscribe_token")}),
        ("Dates", {"fields": ("confirmed_at", "unsubscribed_at", "created_at", "updated_at")}),
        ("Engagement", {"fields": ("bounce_count",)}),
    )


@admin.register(NewsletterCampaign)
class NewsletterCampaignAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "sent_count", "failed_count", "scheduled_at")
    list_filter = ("status", "created_at", "scheduled_at", "sent_at")
    search_fields = ("title", "subject")
    readonly_fields = ("sent_count", "failed_count", "created_at", "updated_at", "sent_at")
    fieldsets = (
        (None, {"fields": ("title", "subject", "status")}),
        ("Content", {"fields": ("html_body", "text_body")}),
        ("Scheduling", {"fields": ("scheduled_at",)}),
        ("Delivery", {"fields": ("sent_count", "failed_count", "sent_at", "created_at", "updated_at")}),
    )
