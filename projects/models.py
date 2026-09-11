from django.db import models
from django.urls import reverse

from common.models import TimestampedModel
from common.utils import unique_slug


class Category(TimestampedModel):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(TimestampedModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Project(TimestampedModel):
    STATUS_CHOICES = [("in_progress", "In progress"), ("completed", "Completed"), ("archived", "Archived")]
    title = models.CharField(max_length=180)
    slug = models.SlugField(unique=True, blank=True)
    summary = models.CharField(max_length=260)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="projects")
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")
    tech_stack = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="completed")
    featured = models.BooleanField(default=False)
    github_url = models.URLField(blank=True)
    demo_url = models.URLField(blank=True)
    impact_metric = models.CharField(max_length=120, blank=True)
    views_count = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self, self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("projects:detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.title


class GalleryImage(TimestampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="gallery")
    image_url = models.URLField()
    caption = models.CharField(max_length=180, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "created_at")
