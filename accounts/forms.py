from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile, User


class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("headline", "bio", "location", "github_url", "linkedin_url", "website_url", "availability")
        widgets = {"bio": forms.Textarea(attrs={"rows": 5})}