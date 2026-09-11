from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm
from .models import Post


def post_list(request):
    posts = Post.objects.filter(status="published").select_related("author").prefetch_related("tags")
    page = Paginator(posts, 8).get_page(request.GET.get("page"))
    return render(request, "blog/list.html", {"page": page})


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author").prefetch_related("tags", "comments__author"), slug=slug, status="published")
    Post.objects.filter(pk=post.pk).update(views_count=F("views_count") + 1)
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect(f"/accounts/login/?next={request.path}")
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post, comment.author = post, request.user
            comment.save()
            messages.success(request, "Comment added.")
            return redirect(post.get_absolute_url())
    return render(request, "blog/detail.html", {"post": post, "form": form})
