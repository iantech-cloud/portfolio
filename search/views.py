from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post
from projects.models import Project

def search(request):
    query = request.GET.get('q', '').strip()
    posts = Post.objects.filter(title__icontains=query, status='published') if query else Post.objects.none()
    projects = Project.objects.filter(title__icontains=query) if query else Project.objects.none()
    results = list(posts) + list(projects)
    page = Paginator(results, 12).get_page(request.GET.get('page'))
    return render(request, 'search/results.html', {'query': query, 'page': page, 'results': results})
