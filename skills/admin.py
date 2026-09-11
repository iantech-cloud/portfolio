from django.contrib import admin

from .models import Certification, Education, Experience, Skill, SkillCategory


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ("name", "issuer", "issued_date", "has_badge", "has_credential")
    list_filter = ("issuer",)
    search_fields = ("name", "issuer")

    @admin.display(boolean=True, description="Badge")
    def has_badge(self, obj):
        return bool(obj.badge_image_url)

    @admin.display(boolean=True, description="Credential")
    def has_credential(self, obj):
        return bool(obj.credential_url)


admin.site.register((SkillCategory, Skill, Experience, Education))
