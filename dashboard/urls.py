from django.urls import path
from . import views
app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard, name='home'),
    path('blog/', views.blog_manager, name='blog'),
    path('projects/', views.project_manager, name='projects'),
    path('media/', views.media_manager, name='media'),
    path('contacts/', views.contact_inbox, name='contacts'),
    path('subscribers/', views.subscribers, name='subscribers'),
    path('comments/', views.comments, name='comments'),
]
