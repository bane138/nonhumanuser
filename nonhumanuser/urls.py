"""nonhumanuser URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from app.views import IndexView, ProfileView, SearchView
from blog.views import StoriesView, StoryView, ArticleView, ArticlesView,\
ArticlesCommentView, StoriesCommentView

from nonhumanuser import settings

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^stories/$', StoriesView.as_view(), name="stories"),
    url(r'^stories/(?P<slug>[\w-]+)/$', StoryView.as_view(), name="story"),
    url(r'^stories/(?P<slug>[\w-]+)/comment/$', StoriesCommentView.as_view(), 
        name='story comment'),
    url(r'^articles/$', ArticlesView.as_view(), name="articles"),
    url(r'^articles/(?P<slug>[\w-]+)/$', ArticleView.as_view(), name="article"),
    url(r'^articles/(?P<slug>[\w-]+)/comment/$', ArticlesCommentView.as_view(), 
        name='article comment'),
    url(r'^library/', include('library.urls')),
    url(r'^media/library/', include('library.urls')),
    url(r'^media/actual_play/', include('actual_play.urls')),
    url(r'^actual_play/', include('actual_play.urls')),
    url(r'^members/', include('django.contrib.auth.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^accounts/profile/(?P<slug>[\-\w]+)/$', ProfileView.as_view(), 
        name='update_user'),
    url(r'^search/(?P<q>.*)$', SearchView.as_view(), name='search'),
]

#if settings.DEBUG:
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
        }))

#if settings.DEBUG:
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
