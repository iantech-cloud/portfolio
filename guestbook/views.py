from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import GuestbookEntryForm
from .models import GuestbookEntry


def index(request):
    entries = GuestbookEntry.objects.filter(is_visible=True).select_related("author")
    form = GuestbookEntryForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("accounts:login")
        if form.is_valid():
            entry = form.save(commit=False)
            entry.author = request.user
            entry.save()
            messages.success(request, "Your note was added to the guestbook.")
            return redirect("guestbook:index")
    return render(request, "guestbook/index.html", {"entries": entries, "form": form})
