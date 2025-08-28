"""nonhumanuser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import path, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path, re_path
from django.contrib import admin
from django.views.static import serve
from app.views import IndexView, ProfileView, SearchView
from blog.views import StoriesView, StoryView, StoryArchiveView, ArticleView, ArticlesView, ArticleArchiveView,\
ArticlesCommentView, StoriesCommentView

from nonhumanuser import settings

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('stories/', StoriesView.as_view(), name="stories"),
    path('stories/story_archive/', StoryArchiveView.as_view(), name="story-archive"),
    re_path(r'^stories/(?P<slug>[\w-]+)/$', StoryView.as_view(), name="story"),
    re_path(r'^stories/(?P<slug>[\w-]+)/comment/$', StoriesCommentView.as_view(), 
        name='story comment'),
    path('articles/', ArticlesView.as_view(), name="articles"),
    path('articles/article_archive/', ArticleArchiveView.as_view(), name="article-archive"),
    re_path(r'^articles/(?P<slug>[\w-]+)/$', ArticleView.as_view(), name="article"),
    re_path(r'^articles/(?P<slug>[\w-]+)/comment/$', ArticlesCommentView.as_view(), 
        name='article comment'),
    path('media/library/', include('library.urls')),
    path('library/', include('library.urls')),
    path('media/actual_play/', include('actual_play.urls')),
    path('actual_play/', include('actual_play.urls')),
    path('members/', include('django.contrib.auth.urls')),
    path('accounts/', include('django_registration.backends.one_step.urls')),
    re_path(r'^accounts/profile/(?P<slug>[\-\w]+)/$', ProfileView.as_view(), 
        name='update_user'),
    re_path(r'^search/(?P<q>.*)$', SearchView.as_view(), name='search'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT
            }),
        ]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL,
        document_root=settings.STATIC_ROOT)
