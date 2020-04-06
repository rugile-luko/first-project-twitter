from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q


def home(request):
    users = models.User.objects.exclude(id=request.user.id).order_by('username')
    form = None

    if request.user.is_authenticated:
        following = request.user.profile.following.all()
        tweets = models.Tweet.objects.filter(Q(created_by__in=following) | Q(created_by=request.user))
        form = forms.TweetForm()

        if "q" in request.GET:
            tweets = tweets.filter(message__icontains=request.GET.get('q'))

        if "hashtag" in request.GET:
            tweets = tweets.filter(message__icontains="#" + request.GET.get('hashtag'))

        if request.method == 'POST':
            form = forms.TweetForm(request.POST)
            if form.is_valid():
                new_tweet = form.save(commit=False)
                new_tweet.created_by = request.user
                new_tweet.save()

                return redirect('home')
            else:
                print(form.errors)

        sort = request.GET.get('sort', None)
        if sort is not None:
            if sort.lower() == 'newtoold':
                tweets = tweets.order_by('-created_at')
            elif sort.lower() == 'oldtonew':
                tweets = tweets.order_by('created_at')
            else:
                tweets = tweets.order_by('-created_at')

    else:
        tweets = models.Tweet.objects.all()

    page = request.GET.get('page', 1)
    paginator = Paginator(tweets, 5)

    try:
        all_tweets = paginator.page(page)
    except PageNotAnInteger:
        all_tweets = paginator.page(1)
    except EmptyPage:
        all_tweets = paginator.page(paginator.num_pages)

    context = {
        "tweets": tweets,
        'all_tweets': all_tweets,
        'users': users,
        'form': form
    }

    return render(request, 'home.html', context)


# @login_required
# def edit_tweet(request, pk):
#     tweet = models.Tweet.objects.get(pk=pk)
#     if request.user != tweet.created_by:
#         return redirect('home')
#
#     if request.method == 'POST':
#         form = forms.TweetForm(request.POST, instance=tweet)
#         if form.is_valid():
#             other_tweet = form.save(commit=False)
#             other_tweet.created_by = request.user
#             other_tweet.save()
#
#         return redirect('home')
#
#     context = {
#         'form': forms.TweetForm(instance=tweet)
#     }
#
#     return render(request, 'create_tweet.html', context)


def detail_tweet(request, pk):
    tweet = get_object_or_404(models.Tweet, pk=pk)
    form = None

    if request.user.is_authenticated:
        if request.method == "POST":
            form = forms.CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.comment_author = request.user
                comment.tweet = tweet
                comment.save()
                return redirect('detail_tweet', pk=pk)
        else:
            form = forms.CommentForm()

    context = {
        'tweet': tweet,
        'is_favorite': tweet.is_favorite(request.user),
        'form': form
    }

    return render(request, "detail_tweet.html", context)


@login_required
@csrf_exempt
def ajax_favorite_tweet(request, pk):
    tweet = get_object_or_404(models.Tweet, pk=pk)
    if tweet.favorite_tweet.filter(id=request.user.id).exists():
        tweet.favorite_tweet.remove(request.user)
    else:
        tweet.favorite_tweet.add(request.user)

    return HttpResponse(status=200)


@login_required
@csrf_exempt
def ajax_comment_like(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    if comment.comment_like.filter(id=request.user.id).exists():
        comment.comment_like.remove(request.user)
    else:
        comment.comment_like.add(request.user)

    return HttpResponse(status=200)





