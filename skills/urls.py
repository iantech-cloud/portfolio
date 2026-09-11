from django.urls import path

from . import views

app_name = "skills"

urlpatterns = [
    path("", views.resume, name="resume"),
    path("resume.pdf", views.resume_pdf, name="resume_pdf"),
]