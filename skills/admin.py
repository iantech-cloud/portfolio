from django.contrib import admin

from .models import Certification, Education, Experience, Skill, SkillCategory


admin.site.register((SkillCategory, Skill, Experience, Education, Certification))
