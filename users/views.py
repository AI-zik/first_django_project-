from cmath import log
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from users.models import Profile
from blog.models import Post
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Your account has been created successfully!")
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {'form': form})

def profile(request, username):
    profile_owner = User.objects.get(username=username)
    user_posts = Post.objects.filter(author_id=profile_owner.id).order_by("-date_posted")
    post_page = request.GET.get("page", 1)
    paginator = Paginator(user_posts, 5)
    page_obj = paginator.get_page(post_page)
    context = {
        "profile_owner" : profile_owner,
        "page_obj" : page_obj
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, "Your account has been updated")
                return redirect("profile", user_id=request.user.id)
        else: 
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context["u_form"] = u_form
        context["p_form"] = p_form
    return render(request, 'users/profile.html', context)
