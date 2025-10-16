from django.urls import path
from blog.views import IndexView, StoriesView, StoryView, ArticleView, ArticleView

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
]