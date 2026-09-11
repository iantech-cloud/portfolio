from django.urls import path

from . import views

app_name = "upwork"

urlpatterns = [
    path("", views.brief_list, name="list"),
    path("new/", views.create_brief, name="create"),
    path("<slug:slug>/", views.brief_detail, name="detail"),
    path("<slug:slug>/submit/", views.submit_solution, name="submit"),
    path("solution/<int:solution_id>/vote/", views.vote_solution, name="vote"),
    path("solution/<int:solution_id>/select/", views.select_solution, name="select"),
]