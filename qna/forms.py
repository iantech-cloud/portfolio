from django import forms

from .models import Answer, Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("title", "body", "tags")
        widgets = {"body": forms.Textarea(attrs={"rows": 10})}


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 8, "placeholder": "Share the reasoning, code, and trade-offs..."})}