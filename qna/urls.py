from django.urls import path

from . import views

app_name = "qna"

urlpatterns = [
    path("", views.question_list, name="list"),
    path("ask/", views.ask_question, name="ask"),
    path("<slug:slug>/", views.question_detail, name="detail"),
    path("<slug:slug>/answer/", views.answer_question, name="answer"),
    path("<slug:slug>/vote/", views.vote_question, name="vote_question"),
    path("answer/<int:answer_id>/vote/", views.vote_answer, name="vote_answer"),
    path("answer/<int:answer_id>/accept/", views.accept_answer, name="accept_answer"),
]