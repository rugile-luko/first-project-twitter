from django.urls import path
from tweets import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tweet/<pk>/detail/', views.detail_tweet, name='detail_tweet'),
    path('ajax/tweet/<pk>/favorite/', views.ajax_favorite_tweet, name='ajax_favorite_tweet'),
    path('ajax/comment/<pk>/like/', views.ajax_comment_like, name='ajax_comment_like'),
    # path('search/', tweet_views.SearchListView.as_view(template_name='search.html'), name='search'),
]
