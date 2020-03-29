from django import template
from ..models import Tweet, Comment
from django.contrib.auth.models import User
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('latest_tweets.html')
def show_latest_tweets(count=5):
    latest_tweets = Tweet.objects.order_by('-created_at')[:count]
    return {'latest_tweets': latest_tweets}


@register.filter
def is_favorite(tweet, user):
    return tweet.is_favorite(user)


@register.filter
def like_comment(comment, user):
    result = comment.like_comment(user)
    return result
