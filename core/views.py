from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.html import escape

from blog.models import Post
from projects.models import Project
from skills.models import Certification, Education, Experience, Skill, SkillCategory

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
        "experience": Experience.objects.all()[:6],
        "education": Education.objects.all(),
        "categories": SkillCategory.objects.prefetch_related("skills"),
        "certifications": Certification.objects.all(),
    })


def certificates(request):
    return render(request, "core/certificates.html", {
        "site": SiteSettings.objects.first(),
        "certifications": Certification.objects.all(),
        "categories": SkillCategory.objects.prefetch_related("skills"),
    })


def robots(request):
    return HttpResponse(f"User-agent: *\nAllow: /\nSitemap: {request.build_absolute_uri(reverse('core:sitemap'))}\n", content_type="text/plain")


def sitemap(request):
    urls = [request.build_absolute_uri(reverse(name)) for name in ("core:home", "core:about", "core:contact", "projects:list", "skills:resume")]
    urls += [request.build_absolute_uri(project.get_absolute_url()) for project in Project.objects.all()]
    body = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" + "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">" + "".join(f"<url><loc>{escape(url)}</loc></url>" for url in urls) + "</urlset>"
    return HttpResponse(body, content_type="application/xml")


def custom_error(request, status):
    return render(request, f"{status}.html", status=status)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        contact = ContactMessage.objects.create(**form.cleaned_data)
        send_mail(
            subject=f"Portfolio contact: {contact.subject}",
            message=f"From: {contact.name} <{contact.email}>\\n\\n{contact.message}",
            from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, "DEFAULT_FROM_EMAIL") else contact.email,
            recipient_list=[site.email] if (site := SiteSettings.objects.first()) else [contact.email],
            fail_silently=True,
        )
        messages.success(request, "Message received. I’ll get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form, "site": SiteSettings.objects.first()})
