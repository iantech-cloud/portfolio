from django.conf import settings
from django.db import models

from common.models import TimestampedModel


class OpenSourceContribution(TimestampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="open_source_contributions")
    project_name = models.CharField(max_length=180)
    role = models.CharField(max_length=180, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    contributed_on = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-contributed_on", "-created_at")
