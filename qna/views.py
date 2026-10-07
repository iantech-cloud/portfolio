from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AnswerForm, QuestionForm
from .models import Answer, AnswerVote, Question, QuestionVote


def question_list(request):
    query = request.GET.get("q", "")
    questions = Question.objects.select_related("author").prefetch_related("tags")
    if query:
        questions = questions.filter(Q(title__icontains=query) | Q(body__icontains=query))
    page = Paginator(questions, 12).get_page(request.GET.get("page"))
    return render(request, "qna/list.html", {"page": page, "query": query})


@login_required
def ask_question(request):
    form = QuestionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        question = form.save(commit=False)
        question.author = request.user
        question.save()
        form.save_m2m()
        return redirect(question.get_absolute_url())
    return render(request, "qna/form.html", {"form": form, "title": "Ask a technical question"})


def question_detail(request, slug):
    question = get_object_or_404(Question.objects.select_related("author").prefetch_related("tags", "answers__author"), slug=slug)
    Question.objects.filter(pk=question.pk).update(views_count=F("views_count") + 1)
    return render(request, "qna/detail.html", {"question": question, "answer_form": AnswerForm()})


@login_required
def answer_question(request, slug):
    question = get_object_or_404(Question, slug=slug, status__in=("open", "answered"))
    form = AnswerForm(request.POST)
    if form.is_valid():
        answer = form.save(commit=False)
        answer.question, answer.author = question, request.user
        answer.save()
        Question.objects.filter(pk=question.pk).update(answer_count=F("answer_count") + 1, status="answered")
    return redirect(question.get_absolute_url())


def _vote(request, model, target, vote_field, counter_field):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login_required", "login_url": f"/accounts/login/?next={request.path}"}, status=401)
    if target.author_id == request.user.id:
        return JsonResponse({"error": "self_vote"}, status=403)
    with transaction.atomic():
        vote, created = model.objects.get_or_create(**{target._meta.model_name: target, "user": request.user}, defaults={"value": 1})
        if not created:
            vote.delete()
            delta = -1
        else:
            delta = 1
        target.__class__.objects.filter(pk=target.pk).update(**{counter_field: F(counter_field) + delta})
        target.refresh_from_db(fields=[counter_field])
    return JsonResponse({"count": getattr(target, counter_field)})


@login_required
def vote_question(request, slug):
    question = get_object_or_404(Question, slug=slug)
    return _vote(request, QuestionVote, question, "value", "vote_count")


@login_required
def vote_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    return _vote(request, AnswerVote, answer, "value", "vote_count")


@login_required
def accept_answer(request, answer_id):
    answer = get_object_or_404(Answer.objects.select_related("question"), pk=answer_id)
    if answer.question.author_id != request.user.id:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied
    with transaction.atomic():
        Answer.objects.filter(question=answer.question).update(is_accepted=False)
        Answer.objects.filter(pk=answer.pk).update(is_accepted=True)
        Question.objects.filter(pk=answer.question_id).update(status="answered")
    return redirect(answer.question.get_absolute_url())
