from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from core.models import SiteSettings

from .models import Certification, Education, Experience, SkillCategory


def resume_context():
    return {
        "site": SiteSettings.objects.first(),
        "categories": SkillCategory.objects.prefetch_related("skills"),
        "experience": Experience.objects.all(),
        "education": Education.objects.all(),
        "certifications": Certification.objects.all(),
    }


def resume(request):
    return render(request, "skills/resume.html", resume_context())


def resume_pdf(request):
    data = resume_context()
    site = data["site"]
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 54
    pdf.setTitle(f"{site.site_name if site else 'Portfolio'} resume")
    pdf.setFont("Helvetica-Bold", 22)
    pdf.drawString(48, y, site.site_name if site else "Technical Portfolio")
    y -= 28
    pdf.setFont("Helvetica", 11)
    pdf.drawString(48, y, site.role if site else "Python engineer & ML builder")
    y -= 32
    for experience in data["experience"]:
        pdf.setFont("Helvetica-Bold", 12)
        pdf.drawString(48, y, f"{experience.role} · {experience.company}")
        y -= 16
        pdf.setFont("Helvetica", 9)
        for line in experience.description.splitlines()[:3]:
            pdf.drawString(60, y, line[:105])
            y -= 13
        y -= 10
        if y < 80:
            pdf.showPage()
            y = height - 54
    pdf.save()
    response = HttpResponse(buffer.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="iano-resume.pdf"'
    return response
