from django import forms

from .models import GuestbookEntry


class GuestbookEntryForm(forms.ModelForm):
    class Meta:
        model = GuestbookEntry
        fields = ("message",)
        widgets = {"message": forms.Textarea(attrs={"rows": 4, "placeholder": "Leave a note..."})}
