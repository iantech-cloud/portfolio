from django.conf import settings
from django.db import models
from common.models import TimestampedModel

class MediaAsset(TimestampedModel):
    file = models.FileField(upload_to='media/%Y/%m/')
    title = models.CharField(max_length=220, blank=True)
    alt_text = models.CharField(max_length=220, blank=True)
    caption = models.CharField(max_length=320, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    def __str__(self): return self.title or self.file.name
