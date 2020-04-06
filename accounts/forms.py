from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=100, required=True, widget=forms.EmailInput())
    username = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 1}
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("This username is taken.")
        return data

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email is already used.")
        return data

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.CharField(
        widget=forms.EmailInput(),
        max_length=100, required=True,
        help_text='Enter your email'
    )

    class Meta:
        model = User
        fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'image']

        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 5, 'placeholder': 'Tell us something about yourself'}
            )
        }


class ContactForm(forms.Form):
    name = forms.CharField(max_length=50, label='Name')
    email = forms.EmailField(max_length=100, label='Email')
    comment = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 10, 'placeholder': 'Enter your comment here'}),
        max_length=2000,
        help_text='The max length of your message is 2000 symbols.'
    )


