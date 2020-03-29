"""twitterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from tweets import views as tweet_views
from accounts import views as account_views
from trending import views as trending_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tweet_views.home, name='home'),
    path('tweet/create/', tweet_views.create_tweet, name='create_tweet'),
    path('tweet/<pk>/edit/', tweet_views.edit_tweet, name='edit_tweet'),
    path('tweet/<pk>/detail/', tweet_views.detail_tweet, name='detail_tweet'),
    path('ajax/tweet/<pk>/favorite/', tweet_views.ajax_favorite_tweet, name='ajax_favorite_tweet'),
    path('ajax/comment/<pk>/like/', tweet_views.ajax_comment_like, name='ajax_comment_like'),
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/<username>', account_views.profile, name='profile'),
    path('search/', tweet_views.SearchListView.as_view(template_name='search.html'), name='search'),
    path('hashtag/<word>/', tweet_views.SearchListView.as_view(template_name='search.html'), name='tweets_by_hashtag'),
    path('follow/<username>/', account_views.follow, name='follow'),
    path('unfollow/<username>/', account_views.unfollow, name='unfollow'),
    path('contact/', account_views.contactview, name='contact'),
    # path('trending/', trending_views.trending, name='trending')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)