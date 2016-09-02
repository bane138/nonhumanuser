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
		catetory = 1
		stories = Entry.objects.filter(category=catetory, active=True, 
			publish_date__lte=datetime.datetime.now())[0:5]
		items_recent = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-created_date')
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'stories': stories, 'items_recent': items_recent, 
			'items_popular': items_popular})


class StoryView(View):
	template = 'blog/story.html'

	def get(self, request, *args, **kwargs):
		story = Entry.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'story': story})


class ArticlesView(View):
	template = 'blog/articles.html'

	def get(self, request):
		catetory = 2
		articles = Entry.objects.filter(category__exact=catetory, active=True, 
			publish_date__lte=datetime.datetime.now())[0:5]
		items_recent = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-created_date')
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'articles': articles})


class ArticleView(View):
	template = 'blog/article.html'

	def get(self, request, *args, **kwargs):
		article = Entry.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'article': article})