from django.conf.urls import url
from blog.views import IndexView, StoriesView, StoryView, ArticleView, ArticleView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
]