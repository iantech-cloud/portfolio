from django.db import models

from common.models import TimestampedModel


class SkillCategory(TimestampedModel):
    name = models.CharField(max_length=80)
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("order", "name")


class Skill(TimestampedModel):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=100)
    level = models.PositiveSmallIntegerField(default=80)
    years = models.DecimalField(max_digits=3, decimal_places=1, default=1)

    class Meta:
        ordering = ("-level", "name")


class Experience(TimestampedModel):
    role = models.CharField(max_length=180)
    company = models.CharField(max_length=180)
    location = models.CharField(max_length=120, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    stack = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ("-start_date",)


class Education(TimestampedModel):
    institution = models.CharField(max_length=180)
    degree = models.CharField(max_length=180)
    field = models.CharField(max_length=180, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    details = models.TextField(blank=True)

    class Meta:
        ordering = ("-start_date",)


class Certification(TimestampedModel):
    name = models.CharField(max_length=180)
    issuer = models.CharField(max_length=180)
    issued_date = models.DateField()
    credential_url = models.URLField(
        blank=True,
        help_text="Public verification page, such as a Credly public_url.",
    )
    badge_image_url = models.URLField(
        blank=True,
        help_text="Direct HTTPS image URL for the badge artwork. Optional; a safe fallback is shown when unavailable.",
    )
    badge_alt = models.CharField(
        max_length=180,
        blank=True,
        help_text="Accessible description for the badge image.",
    )

    class Meta:
        ordering = ("-issued_date",)
