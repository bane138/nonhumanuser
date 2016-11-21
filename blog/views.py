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
		category = Category.objects.get(name="Stories")
		stories = Entry.objects.filter(category__name='Stories', active=True,
			publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
		items_recent = Entry.objects.filter(category__name='Stories', active=True,
											publish_date__lte=datetime.datetime.now())\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category__name='Stories', active=True,
											 publish_date__lte=datetime.datetime.now())\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {
			'section': {
				'name': 'Stories'
			},
			'category': category,
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/stories/',
			'og_title': category.name,
			'og_description': category.description,
			'og_image': 'http://www.nonhumanuser.com/images/Stories.png',
			'stories': stories, 'items_recent': items_recent,
			'items_popular': items_popular, 'links': links,
			'count': stories.count(),
			'icon_class': 'lg_icon_class_stories'})


class StoryView(View):
	template = 'blog/story.html'

	def get(self, request, *args, **kwargs):
		category = Category.objects.get(name='Stories')
		story = Entry.objects.get(slug=self.kwargs['slug'])
		items_recent = Entry.objects.filter(category__name='Stories', active=True,
											publish_date__lte=datetime.datetime.now())\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category__name='Stories', active=True,
											 publish_date__lte=datetime.datetime.now())\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		form = EntryCommentForm(request.POST)
		story_comments = story.comments.all()
		story.number_comments = story_comments.count()
		story.number_views = story.number_views + 1
		story.save()
		return render(request, self.template, {
			'section': {
				'name': 'Stories'
			},
			'category': category,
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/stories/' + story.slug + '/',
			'og_title': story.title,
			'og_description': story.description,
			'og_image': 'http://www.nonhumanuser.com' + story.image.url if story.image else '',
			'story': story, 'items_recent': items_recent,
			'items_popular': items_popular, 'links': links, 'form': form,
			'comments': story_comments, 'icon_class': 'lg_icon_class_stories'})


class StoriesCommentView(View):
	template = 'blog/story.html'

	def post(self, request, *args, **kwargs):
		form = EntryCommentForm(request.POST)

		if form.is_valid():
			comment = form.cleaned_data['comment']
			user = request.user
			entry = Entry.objects.get(pk=request.POST.get('entry_id'))
			instance = EntryComment(comment=comment, user=user, entry=entry)
			instance.save()

		return HttpResponseRedirect(
			'/stories/' + kwargs['slug'] + '/')


class StoryArchiveView(View):
	template = 'blog/story_list.html'

	def get(self, request, *args, **kwargs):
		items_recent = Entry.objects.filter(active=True, category__name='Stories',
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(active=True, category__name='Stories',
											publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		stories = Entry.objects.filter(active=True, category__name='Stories',
									   publish_date__lte=datetime.datetime.now()).order_by('-created_date')
		links = get_main_links()
		context = {
			'section': { 'name': 'Stories' }
		}
		context['og_type'] = 'webpage'
		context['og_url'] = 'http://www.nonhumanuser.com/stories/story_archive/'
		context['og_title'] = 'Story Archive'
		context['og_description'] = 'Horror stories in the tradition of H.P. Lovecraft and the Cthulhu Mythos'
		context['og_image'] = 'http://www.nonhumanuser.com//images/Stories.png'
		context['items_recent'] = items_recent
		context['items_popular'] = items_popular
		context['links'] = links
		context['icon_class'] = 'lg_icon_class_stories'
		context['stories'] = stories

		return render(request, self.template, context)


class ArticlesView(View):
	template = 'blog/articles.html'

	def get(self, request):
		category = Category.objects.get(name='Articles')
		articles = Entry.objects.filter(category__name='Articles', active=True,
			publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
		items_recent = Entry.objects.filter(category__name='Articles', active=True,
											publish_date__lte=datetime.datetime.now())\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category__name='Articles', active=True,
											 publish_date__lte=datetime.datetime.now())\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {
			'section': {
				'name': 'Articles'
			},
			'category': category,
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/articles/',
			'og_title': category.name,
			'og_description': category.description,
			'og_image': 'http://www.nonhumanuser.com/images/Articles.png',
			'articles': articles, 'items_recent': items_recent,
			'items_popular': items_popular, 'links': links,
			'count': articles.count(),
			'icon_class': 'lg_icon_class_articles'})


class ArticleView(View):
	template = 'blog/article.html'

	def get(self, request, *args, **kwargs):
		category = Category.objects.get(name='Articles')
		article = Entry.objects.get(slug=self.kwargs['slug'])
		items_recent = Entry.objects.filter(category__name='Articles', active=True,
											publish_date__lte=datetime.datetime.now())\
		.order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(category__name='Articles', active=True,
											 publish_date__lte=datetime.datetime.now())\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		form = EntryCommentForm(request.POST)
		article_comments = article.comments.all()
		article.number_comments = article_comments.count()
		article.number_views = article.number_views + 1
		article.save()
		return render(request, self.template, {
			'section': {
				'name': 'Articles'
			},
			'category': category,
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/stories/' + article.slug + '/',
			'og_title': article.title,
			'og_description': article.description,
			'og_image': 'http://www.nonhumanuser.com' + article.image.url if article.image else '',
			'article': article, 'items_recent': items_recent,
			'items_popular': items_popular, 'links': links, 'form': form,
			'comments': article_comments, 'icon_class': 'lg_icon_class_articles'})


class ArticlesCommentView(View):
	template = 'blog/article.html'

	def post(self, request, *args, **kwargs):
		form = EntryCommentForm(request.POST)

		if form.is_valid():
			comment = form.cleaned_data['comment']
			user = request.user
			entry = Entry.objects.get(pk=request.POST.get('entry_id'))
			instance = EntryComment(comment=comment, user=user, entry=entry)
			instance.save()

		return HttpResponseRedirect(
			'/articles/' + kwargs['slug'] + '/')


class ArticleArchiveView(View):
	template = 'blog/article_list.html'

	def get(self, request, *args, **kwargs):
		items_recent = Entry.objects.filter(active=True, category__name='Articles',
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Entry.objects.filter(active=True, category__name='Articles',
											publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		articles = Entry.objects.filter(active=True, category__name='Articles',
									   publish_date__lte=datetime.datetime.now()).order_by('-created_date')
		links = get_main_links()
		context = {
			'section': { 'name': 'Articles' }
		}
		context['og_type'] = 'webpage'
		context['og_url'] = 'http://www.nonhumanuser.com/articles/article_archive/'
		context['og_title'] = 'Article Archive'
		context['og_description'] = 'Articles and observations about the Call of Cthulhu role playing game.'
		context['og_image'] = 'http://www.nonhumanuser.com//images/Articles.png'
		context['items_recent'] = items_recent
		context['items_popular'] = items_popular
		context['links'] = links
		context['icon_class'] = 'lg_icon_class_articles'
		context['articles'] = articles

		return render(request, self.template, context)