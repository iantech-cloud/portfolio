from django.urls import path
from . import views

app_name = "newsletter"

urlpatterns = [
    path("subscribe/", views.subscribe, name="subscribe"),
    path("confirm/<str:token>/", views.confirm_subscription, name="confirm"),
    path("unsubscribe/<str:token>/", views.unsubscribe, name="unsubscribe"),
    path("archive/", views.archive, name="archive"),
    path("archive/<int:pk>/", views.campaign_detail, name="campaign_detail"),
]
