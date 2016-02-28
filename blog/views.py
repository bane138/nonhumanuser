from django.shortcuts import render
from django.views.generic import View
from blog.models import Blog, Entry, Category

# Create your views here.
class IndexView(View):
	def get(self, request):
		entries = Entry.objects.all()
		return render(request, 'blog/index.html', {'section': {'name': 'Blog'}, 
			'entries': entries})


class StoriesView(View):
	template = 'blog/stories.html'

	def get(self, request):
		stories = Entry.objects.filter(blog__exact=1)
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'stories': stories})


class StoryView(View):
	template = 'blog/story.html'

	def get(self, request, *args, **kwargs):
		story = Entry.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Stories'}, 
			'story': story})


class ArticlesView(View):
	template = 'blog/articles.html'

	def get(self, request):
		articles = Entry.objects.filter(blog__exact=2)
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'articles': articles})


class ArticleView(View):
	template = 'blog/article.html'

	def get(self, request, *args, **kwargs):
		article = Entry.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Articles'}, 
			'article': article})