from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import TimestampedModel


class User(AbstractUser):
    email = models.EmailField(unique=True)
    reputation = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ("-date_joined",)


class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    headline = models.CharField(max_length=180, default="Software engineer & ML builder")
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=120, blank=True)
    github_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    availability = models.CharField(max_length=120, default="Open to interesting problems")

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s profile"


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
