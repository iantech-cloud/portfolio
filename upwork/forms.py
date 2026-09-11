from django import forms

from .models import Brief, Solution


class BriefForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = ("title", "description", "budget", "stack")
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ("approach", "body")
        widgets = {"approach": forms.Textarea(attrs={"rows": 4}), "body": forms.Textarea(attrs={"rows": 8})}