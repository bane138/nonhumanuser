from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from blog.models import Blog, Entry, Category, EntryComment
from nonhumanuser.utils import *
from .forms import EntryCommentForm
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
			'items_popular': items_popular, 'links': links, 
			'icon_class': 'lg_icon_class_stories'})


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
		form = EntryCommentForm(request.POST)
		story_comments = story.comments.all()
		story.number_comments = story_comments.count()
		story.number_views = story.number_views + 1
		story.save()
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'story': story, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links, 'form': form, 
			'comments': story_comments, 'icon_class': 'lg_icon_class_stories'})


class StoriesCommentView(View):
	template = 'blog/story.html'

	def post(self, request, *args, **kwargs):
		form = EntryCommentForm(request.POST)

		if form.is_valid():
			body = form.cleaned_data['body']
			author = request.user.username
			user = request.user
			entry = Entry.objects.get(pk=request.POST.get('entry_id'))
			instance = EntryComment(body=body, author=author, entry=entry)
			instance.save()

		return HttpResponseRedirect(
			'/stories/' + kwargs['slug'] + '/')


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
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'articles': articles, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links, 
			'icon_class': 'lg_icon_class_articles'})


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
		form = EntryCommentForm(request.POST)
		article_comments = article.comments.all()
		article.number_comments = article_comments.count()
		article.number_views = article.number_views + 1
		article.save()
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'article': article, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links, 'form': form, 
			'comments': article_comments, 'icon_class': 'lg_icon_class_articles'})


class ArticlesCommentView(View):
	template = 'blog/article.html'

	def post(self, request, *args, **kwargs):
		form = EntryCommentForm(request.POST)

		if form.is_valid():
			body = form.cleaned_data['body']
			author = request.user.username
			user = request.user
			entry = Entry.objects.get(pk=request.POST.get('entry_id'))
			instance = EntryComment(body=body, author=author, entry=entry)
			instance.save()

		return HttpResponseRedirect(
			'/articles/' + kwargs['slug'] + '/')