from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from blog.models import Post, Comment
from projects.models import Project
from core.models import ContactMessage
from newsletter.models import NewsletterSubscriber
from media_library.models import MediaAsset

@staff_member_required
def dashboard(request):
    stats = {'posts': Post.objects.count(), 'projects': Project.objects.count(), 'contacts': ContactMessage.objects.filter(is_read=False).count(), 'subscribers': NewsletterSubscriber.objects.filter(status='confirmed').count()}
    return render(request, 'dashboard/home.html', {'stats': stats})

@staff_member_required
def blog_manager(request): return render(request, 'dashboard/table.html', {'title': 'Blog Manager', 'items': Post.objects.all()})
@staff_member_required
def project_manager(request): return render(request, 'dashboard/table.html', {'title': 'Project Manager', 'items': Project.objects.all()})
@staff_member_required
def media_manager(request): return render(request, 'dashboard/table.html', {'title': 'Media Library', 'items': MediaAsset.objects.all()})
@staff_member_required
def contact_inbox(request): return render(request, 'dashboard/table.html', {'title': 'Contact Inbox', 'items': ContactMessage.objects.all()})
@staff_member_required
def subscribers(request): return render(request, 'dashboard/table.html', {'title': 'Subscribers', 'items': NewsletterSubscriber.objects.all()})
@staff_member_required
def comments(request): return render(request, 'dashboard/table.html', {'title': 'Comments Moderation', 'items': Comment.objects.all()})
