from django.shortcuts import render
from django.views.generic import View
from blog.models import Blog, Entry, Category
import datetime

# Create your views here.
class IndexView(View):
	def get(self, request):
		entries = Entry.objects.all()
		return render(request, 'blog/index.html', {'section': {'name': 'Blog'}, 
			'entries': entries})


class StoriesView(View):
	template = 'blog/stories.html'

	def get(self, request):
		stories = Entry.objects.filter(category=2,
			publish_date__lte=datetime.datetime.now())[0:5]
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'stories': stories})


class StoryView(View):
	template = 'blog/story.html'

	def get(self, request, *args, **kwargs):
		story = Entry.objects.get(slug=self.kwargs['slug'])
		comments = story.comments_set.all()
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'story': story, 'comments': comments})


class ArticlesView(View):
	template = 'blog/articles.html'

	def get(self, request):
		articles = Entry.objects.filter(category__exact=1, 
			publish_date__lte=datetime.datetime.now())[0:5]
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'articles': articles})


class ArticleView(View):
	template = 'blog/article.html'

	def get(self, request, *args, **kwargs):
		article = Entry.objects.get(slug=self.kwargs['slug'])
		comments = article.comments_set.all()
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'article': article, 'comments': comments})