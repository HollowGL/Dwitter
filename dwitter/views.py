from django.shortcuts import render, redirect, get_object_or_404

from .forms import DweetForm, CommentForm
from .models import Dweet, Profile, Comment


def dashboard(request):
    form = DweetForm(request.POST or None)
    comment_form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect("dwitter:dashboard")
        elif comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.dweet = get_object_or_404(Dweet, id=request.POST.get("dweet_id"))
            comment.save()
            return redirect("dwitter:dashboard")
    
    # Get dweets from users that the current user follows
    # and order them by creation time
    followed_dweets = Dweet.objects.filter(
        user__profile__in=request.user.profile.follows.all()
    ).order_by("-created_at")

    liked_by_followed_all = []
    for dweet in followed_dweets:
        liked_by_followed_all.append({
            "dweet": dweet,
            "liked_by_followed": dweet.likes.filter(profile__in=request.user.profile.follows.all()),
            "liked_by_user": request.user in dweet.likes.all()
        })

    return render(
        request,
        "dwitter/dashboard.html",
        {"form": form, "comment_form": comment_form, "liked_by_followed_all": liked_by_followed_all}
    )


def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user)
    return render(request, "dwitter/profile_list.html", {"profiles": profiles})


def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)
    if request.method == "POST":
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get("follow")
        if action == "follow":
            current_user_profile.follows.add(profile)
        elif action == "unfollow":
            current_user_profile.follows.remove(profile)
        current_user_profile.save()
    return render(request, "dwitter/profile.html", {"profile": profile})


def like_dweet(request, dweet_id):
    dweet = get_object_or_404(Dweet, id=dweet_id)
    if request.user in dweet.likes.all():
        dweet.likes.remove(request.user)
    else:
        dweet.likes.add(request.user)
    return redirect('dwitter:dashboard')
