from django.core.paginator import Paginator
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Project


def project_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    projects = Project.objects.select_related("category").prefetch_related("tags", "gallery")
    if query:
        projects = projects.filter(Q(title__icontains=query) | Q(summary__icontains=query) | Q(description__icontains=query))
    if category:
        projects = projects.filter(category__slug=category)
    page = Paginator(projects, 9).get_page(request.GET.get("page"))
    return render(request, "projects/list.html", {"page": page, "categories": Category.objects.all(), "query": query, "active_category": category})


def project_detail(request, slug):
    project = get_object_or_404(Project.objects.select_related("category").prefetch_related("tags", "gallery"), slug=slug)
    Project.objects.filter(pk=project.pk).update(views_count=F("views_count") + 1)
    return render(request, "projects/detail.html", {"project": project})
