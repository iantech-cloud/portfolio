from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from .models import NewsletterSubscriber, NewsletterCampaign
from .forms import NewsletterSignupForm


@require_http_methods(["POST"])
def subscribe(request):
    form = NewsletterSignupForm(request.POST)
    next_url = request.POST.get("next", "core:home")
    if form.is_valid():
        subscriber = form.save()
        messages.success(request, "Check your email to confirm your subscription.")
        return redirect(next_url)
    else:
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return redirect(next_url)


def confirm_subscription(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, confirmation_token=token)
    if subscriber.status == "confirmed":
        messages.info(request, "You are already subscribed.")
    else:
        subscriber.confirm()
        messages.success(request, "Your subscription is confirmed. Thank you!")
    return redirect("core:home")


def unsubscribe(request, token):
    subscriber = get_object_or_404(NewsletterSubscriber, unsubscribe_token=token)
    subscriber.unsubscribe()
    messages.success(request, "You have been unsubscribed.")
    return redirect("core:home")


def archive(request):
    campaigns = NewsletterCampaign.objects.filter(status="sent").order_by("-sent_at")
    page = Paginator(campaigns, 10).get_page(request.GET.get("page"))
    return render(request, "newsletter/archive.html", {"page": page})


def campaign_detail(request, pk):
    campaign = get_object_or_404(NewsletterCampaign, pk=pk, status="sent")
    return render(request, "newsletter/campaign_detail.html", {"campaign": campaign})
