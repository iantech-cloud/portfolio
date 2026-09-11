from django.utils.text import slugify


def unique_slug(instance, value, field_name="slug"):
    """Create a stable slug on first save without changing it on updates."""
    base = slugify(value) or "item"
    slug = base
    model = instance.__class__
    index = 2
    while model.objects.filter(**{field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base}-{index}"
        index += 1
    return slug