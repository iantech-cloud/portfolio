from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BriefForm, SolutionForm
from .models import Brief, Solution, SolutionVote


def brief_list(request):
    briefs = Brief.objects.filter(status__in=("open", "in_review")).select_related("client")
    page = Paginator(briefs, 10).get_page(request.GET.get("page"))
    return render(request, "upwork/list.html", {"page": page})


@login_required
def create_brief(request):
    form = BriefForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        brief = form.save(commit=False)
        brief.client = request.user
        brief.save()
        return redirect(brief.get_absolute_url())
    return render(request, "upwork/form.html", {"form": form, "title": "Post a client brief"})


def brief_detail(request, slug):
    brief = get_object_or_404(Brief.objects.select_related("client", "selected_solution").prefetch_related("solutions__author"), slug=slug)
    Brief.objects.filter(pk=brief.pk).update(views_count=F("views_count") + 1)
    return render(request, "upwork/detail.html", {"brief": brief, "solution_form": SolutionForm()})


@login_required
def submit_solution(request, slug):
    brief = get_object_or_404(Brief, slug=slug, status__in=("open", "in_review"))
    form = SolutionForm(request.POST)
    if form.is_valid():
        solution = form.save(commit=False)
        solution.brief, solution.author = brief, request.user
        solution.save()
        Brief.objects.filter(pk=brief.pk).update(solution_count=F("solution_count") + 1, status="in_review")
    return redirect(brief.get_absolute_url())


@login_required
def vote_solution(request, solution_id):
    solution = get_object_or_404(Solution, pk=solution_id)
    if solution.author_id == request.user.id:
        return JsonResponse({"error": "self_vote"}, status=403)
    with transaction.atomic():
        vote, created = SolutionVote.objects.get_or_create(solution=solution, user=request.user, defaults={"value": 1})
        if not created:
            vote.delete()
            delta = -1
        else:
            delta = 1
        Solution.objects.filter(pk=solution.pk).update(vote_count=F("vote_count") + delta)
        solution.refresh_from_db(fields=["vote_count"])
    return JsonResponse({"count": solution.vote_count})


@login_required
def select_solution(request, solution_id):
    solution = get_object_or_404(Solution.objects.select_related("brief"), pk=solution_id)
    if not request.user.is_staff and solution.brief.client_id != request.user.id:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    with transaction.atomic():
        Solution.objects.filter(brief=solution.brief).update(is_selected=False)
        Solution.objects.filter(pk=solution.pk).update(is_selected=True)
        Brief.objects.filter(pk=solution.brief_id).update(selected_solution=solution, status="closed")
    return redirect(solution.brief.get_absolute_url())
