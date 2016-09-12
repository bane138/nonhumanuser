from django.shortcuts import render
from django.views.generic import View
from blog.models import Blog, Entry, Category
from nonhumanuser.utils import *
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
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'stories': stories, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class StoryView(View):
	template = 'blog/story.html'

	def get(self, request, *args, **kwargs):
		catetory = 1
		story = Entry.objects.get(slug=self.kwargs['slug'])
		items_recent = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'story': story, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class ArticlesView(View):
	template = 'blog/articles.html'

	def get(self, request):
		catetory = 2
		articles = Entry.objects.filter(category=catetory, active=True, 
			publish_date__lte=datetime.datetime.now())[0:5]
		items_recent = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		print(links)
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'articles': articles, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class ArticleView(View):
	template = 'blog/article.html'

	def get(self, request, *args, **kwargs):
		catetory = 2
		article = Entry.objects.get(slug=self.kwargs['slug'])
		items_recent = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category=catetory, active=True)\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'article': article, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})