from django import forms
from . import models


class TweetForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
        ),
        max_length=140,
    )

    class Meta:
        model = models.Tweet
        fields = ['message']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(
                attrs={'rows': 5, 'placeholder': 'What is on your mind?'}
            )
        }