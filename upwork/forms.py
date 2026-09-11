from django import forms

from .models import Brief, Solution


class BriefForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = ("title", "description", "budget", "stack")
        widgets = {"description": forms.Textarea(attrs={"rows": 8})}


class StudentQuestionForm(forms.ModelForm):
    class Meta:
        model = Brief
        fields = ("title", "description", "math_content", "attachment")
        labels = {
            "title": "What do you need help with?",
            "description": "Describe the problem",
            "math_content": "Formula or working (LaTeX supported)",
            "attachment": "Add an image or file",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 7, "placeholder": "Tell me what you have tried and where you got stuck..."}),
            "math_content": forms.Textarea(attrs={"rows": 4, "placeholder": r"Example: \\[ y = mx + c \\]"}),
        } 

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        if not attachment:
            return attachment

        allowed_types = {
            "image/jpeg": {"jpg", "jpeg"},
            "image/png": {"png"},
            "image/webp": {"webp"},
            "application/pdf": {"pdf"},
            "text/plain": {"txt"},
        }
        if attachment.size > 10 * 1024 * 1024:
            raise forms.ValidationError("Please keep uploads under 10 MB.")

        name = attachment.name or ""
        suffix = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        content_type = (getattr(attachment, "content_type", "") or "").lower()
        allowed_extensions = {extension for extensions in allowed_types.values() for extension in extensions}
        if suffix not in allowed_extensions or content_type not in allowed_types or suffix not in allowed_types[content_type]:
            raise forms.ValidationError("Upload a JPG, PNG, WEBP, PDF, or TXT file.")
        if any(character in name for character in ("/", "\\", "\x00")):
            raise forms.ValidationError("The uploaded filename is not valid.")
        return attachment


class SolutionForm(forms.ModelForm):
    class Meta:
        model = Solution
        fields = ("approach", "body")
        widgets = {"approach": forms.Textarea(attrs={"rows": 4}), "body": forms.Textarea(attrs={"rows": 8})}
