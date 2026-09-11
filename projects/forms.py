from django import forms

from .models import Project


class ProjectFilterForm(forms.Form):
    q = forms.CharField(required=False, label="")
    category = forms.CharField(required=False, label="")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ("title", "summary", "description", "category", "tags", "tech_stack", "status", "featured", "github_url", "demo_url", "impact_metric")