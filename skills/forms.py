from django import forms

from .models import Certification, Education, Experience


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        exclude = ("created_at", "updated_at")


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        exclude = ("created_at", "updated_at")


class CertificationForm(forms.ModelForm):
    class Meta:
        model = Certification
        exclude = ("created_at", "updated_at")