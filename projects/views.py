from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

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


@cache_page(300, key_prefix="project-detail")
@vary_on_headers("Cookie")
def project_detail(request, slug):
    cache_key = f"project-detail:{slug}"
    project = cache.get(cache_key)
    if project is None:
        project = get_object_or_404(
            Project.objects.select_related("category").prefetch_related("tags"),
            slug=slug,
        )
        cache.set(cache_key, project, 300)
    return render(request, "projects/detail.html", {"project": project})
