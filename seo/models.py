from django.db import models
from common.models import TimestampedModel

class PageSeo(TimestampedModel):
    path = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=160)
    canonical_url = models.URLField(blank=True)
    og_image = models.ImageField(upload_to='seo/', blank=True, null=True)
    noindex = models.BooleanField(default=False)
    sitemap_include = models.BooleanField(default=True)
    def __str__(self): return self.path

class Redirect(TimestampedModel):
    source = models.CharField(max_length=255, unique=True)
    destination = models.CharField(max_length=255)
    permanent = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    def __str__(self): return f'{self.source} → {self.destination}'
