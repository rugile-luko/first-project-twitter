from django.db import models
from django.contrib.auth.models import User


class Tweet(models.Model):
    message = models.TextField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, related_name='tweets', on_delete=models.CASCADE)
    favorite_tweet = models.ManyToManyField(User, symmetrical=False, related_name='favorite_tweet', blank=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.message

    def symbols_left(self):
        return 140 - len(self.message)

    def tweet_as_list(self):
        return self.message.split(' ')

    def is_favorite(self, user):
        is_favorite = False
        if self.favorite_tweet.filter(id=user.id).exists():
            is_favorite = True

        return is_favorite


class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='comment', on_delete=models.CASCADE)
    comment = models.TextField(max_length=140, help_text='The max length of your message can be 140 symbols.')
    date_created = models.DateTimeField(auto_now_add=True)
    comment_author = models.ForeignKey(User, null=True, related_name='comment', on_delete=models.CASCADE)
    comment_like = models.ManyToManyField(User, symmetrical=False, related_name='like', blank=True)

    class Meta:
        ordering = ('-date_created', )

    def __str__(self):
        return 'Commented by {}'.format(self.comment_author)

    def comment_as_list(self):
        return self.comment.split(' ')

    def like_comment(self, user):
        like_comment = False
        if self.comment_like.filter(id=user.id).exists():
            like_comment = True

        return like_comment
