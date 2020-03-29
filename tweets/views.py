from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from . import models
from . import forms
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic.list import ListView
from django.db.models import Q


def home(request):
    users = models.User.objects.exclude(id=request.user.id).order_by('username')
    if request.user.is_authenticated:
        following = request.user.profile.following.all()
        tweet = models.Tweet.objects.filter(Q(created_by__in=following) | Q(created_by=request.user)).\
            order_by('-created_at')

        sort = request.GET.get('sort', None)
        if sort is not None:
            if sort.lower() == 'newtoold':
                tweet = tweet.order_by('-created_at')
            elif sort.lower() == 'oldtonew':
                tweet = tweet.order_by('created_at')
            else:
                tweet = tweet.order_by('-created_at')

    else:
        tweet = models.Tweet.objects.all().order_by('-created_at')

    page = request.GET.get('page', 1)
    paginator = Paginator(tweet, 15)
    try:
        all_tweets = paginator.page(page)
    except PageNotAnInteger:
        all_tweets = paginator.page(1)
    except EmptyPage:
        all_tweets = paginator.page(paginator.num_pages)

    return render(request, 'home.html', {"tweet": tweet, 'all_tweets': all_tweets, 'users': users})


@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = forms.TweetForm(request.POST)
        if form.is_valid():
            new_tweet = form.save(commit=False)
            new_tweet.created_by = request.user
            new_tweet.save()

            return redirect('home')

    context = {
        "form": forms.TweetForm()
    }
    return render(request, "create_tweet.html", context)


@login_required
def edit_tweet(request, pk):
    tweet = models.Tweet.objects.get(pk=pk)
    if request.user != tweet.created_by:
        return redirect('home')
    if request.method == 'POST':
        form = forms.TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            other_tweet = form.save(commit=False)
            other_tweet.created_by = request.user
            other_tweet.save()

        return redirect('home')

    context = {
        'form': forms.TweetForm(instance=tweet)
    }

    return render(request, 'create_tweet.html', context)


def detail_tweet(request, pk):
    tweet = get_object_or_404(models.Tweet, pk=pk)
    # comment = models.Comment.objects.all()

    # comment = get_object_or_404(models.Comment)
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
        # 'like_comment': comment.like_comment(request.user),
        'form': form
    }

    return render(request, "detail_tweet.html", context)


# @login_required
# def favorite_tweet(request, pk):
#     tweet = get_object_or_404(models.Tweet, pk=pk)
#     if tweet.favorite_tweet.filter(id=request.user.id).exists():
#         tweet.favorite_tweet.remove(request.user)
#     else:
#         tweet.favorite_tweet.add(request.user)
#
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


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


class SearchListView(ListView):
    model = models.Tweet
    context_object_name = 'tweets'
    template_name = 'search.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = models.Tweet.objects.all()

        word = self.kwargs.get('word', None)
        if word:
            query = "#" + word

        if query:
            return queryset.filter(Q(message__contains=query))
        else:
            return queryset







