from django import forms

from .models import Comment, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 4, "placeholder": "Add a thoughtful comment..."})}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "excerpt", "body", "status", "tags")