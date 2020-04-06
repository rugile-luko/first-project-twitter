from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from tweets.models import Tweet
from django.core.mail import send_mail


def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = forms.SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_tweets = Tweet.objects.filter(created_by=user)

    page = request.GET.get('page', 1)
    paginator = Paginator(user_tweets, 13)

    try:
        user_tweets = paginator.page(page)
    except PageNotAnInteger:
        user_tweets = paginator.page(1)
    except EmptyPage:
        user_tweets = paginator.page(paginator.num_pages)

    if request.user.is_authenticated and request.user == user:
        if request.method == "POST":
            user_tweets = Tweet.objects.filter(created_by=request.user)
            u_form = forms.UserUpdateForm(request.POST, instance=request.user)
            p_form = forms.ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                user.refresh_from_db()
                for user_tweet in user_tweets:
                    user_tweet.save()
                messages.success(request, 'Your account has been updated!')
                return redirect('profile', username=user.username)
        else:
            u_form = forms.UserUpdateForm(instance=request.user)
            p_form = forms.ProfileUpdateForm(instance=request.user.profile)

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'user_tweets': user_tweets,
        }
        return render(request, 'profile.html', context)
    else:
        context = {
            "user": user,
            "user_tweets": user_tweets
        }

    return render(request, 'profile.html', context)


@login_required
def follow(request, username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    user.profile.followers.add(current_user)
    current_user.profile.following.add(user)
    return redirect('profile', username=username)


@login_required
def unfollow(request, username):
    user = get_object_or_404(User, username=username)
    current_user = request.user
    user.profile.followers.remove(current_user)
    current_user.profile.following.remove(user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def favorite(request):
    user = request.user
    user.profile.favorite_tweet.add(user)
    return redirect('home')


def contactview(request):
    form = forms.ContactForm()
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            comment = "User named %s sent the following message: \n\n %s." % (form.cleaned_data.get("name"), form.cleaned_data.get("comment"))
            send_mail('New Message', comment, form.cleaned_data.get("email"), [settings.ADMIN_EMAIL])
            messages.success(request, 'Your message has been sent!')

        return redirect('contact')

    else:
        context = {'form': form}
        return render(request, 'contact.html', context)



