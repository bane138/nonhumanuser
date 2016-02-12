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
from app import views
from blog.views import StoriesView, StoryView, ArticleView, ArticlesView

urlpatterns = [
	url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    url(r'^stories/$', StoriesView.as_view(), name="stories"),
    url(r'^stories/(?P<slug>[\w-]+)/$', StoryView.as_view(), name="story"),
    url(r'^articles/$', ArticlesView.as_view(), name="articles"),
    url(r'^articles/(?P<slug>[\w-]+)/$', ArticleView.as_view(), name="article"),
    url(r'^library/', include('library.urls')),
]
