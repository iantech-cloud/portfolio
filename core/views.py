from django.contrib import messages
from django.shortcuts import redirect, render

from blog.models import Post
from projects.models import Project
from skills.models import Experience, Skill, SkillCategory

from .forms import ContactForm
from .models import ContactMessage, SiteSettings


def home(request):
    site = SiteSettings.objects.first()
    projects = Project.objects.filter(featured=True).prefetch_related("tags", "category")[:3]
    if not projects:
        projects = Project.objects.filter(status="completed").prefetch_related("tags", "category")[:3]
    posts = Post.objects.filter(status="published").prefetch_related("tags")[:3]
    skills = Skill.objects.select_related("category").order_by("-level")[:8]
    return render(request, "core/home.html", {"site": site, "projects": projects, "posts": posts, "skills": skills})


def about(request):
    return render(request, "core/about.html", {
        "site": SiteSettings.objects.first(),
        "experience": Experience.objects.all()[:4],
        "categories": SkillCategory.objects.prefetch_related("skills"),
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        ContactMessage.objects.create(**form.cleaned_data)
        messages.success(request, "Message received. I’ll get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form, "site": SiteSettings.objects.first()})
