from django.shortcuts import render
from django.views.generic import View
from library.models import Item, Stack, ItemComment
from library.forms import ItemCommentForm
from django.core.files.storage import default_storage
from django.http import HttpResponse, HttpResponseRedirect
from nonhumanuser.utils import *
import datetime

# Create your views here.
class IndexView(View):
	def get(self, request):
		stacks = Stack.objects.all()
		items_recent = Item.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Item.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, 'library/index.html', 
			{'section': {'name': 'Library'},
			 'og_type': 'webpage',
			 'og_url': 'http://www.nonhumanuser.com/library/',
			 'og_title': 'Library',
			 'og_description': 'Library of Call of Cthulhu resources.',
			 'og_image': 'http://www.nonhumanuser.com/images/Library.png',
			 'stacks': stacks,
			 'items_recent': items_recent,
			 'items_popular': items_popular,
			 'links': links})


class ItemsView(View):
	template = 'library/items.html'

	def get(self, request, *args, **kwargs):
		stack = Stack.objects.get(slug=self.kwargs['slug'])
		stacks = Stack.objects.all()
		items_total = Item.objects.all()
		items = Item.objects.filter(stack__exact=stack.id, active=True, 
			publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
		items_recent = Item.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Item.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': stack.name},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/library/' + stack.name.lower() + '/',
			'og_title': stack.name,
			'og_description': stack.tagline,
			'og_image': 'http://www.nonhumanuser.com/images/' + stack.name + '.png',
			'items': items,
			'stack': stack,
			'stacks': stacks,
			'items_recent': items_recent,
			'items_popular': items_popular,
			'links': links,
			'count': items_total.count(),
			'icon_class': 'lg_icon_class_library'})


class ItemView(View):
	template = 'library/item.html'

	def get(self, request, *args, **kwargs):
		item = Item.objects.get(slug=self.kwargs['slug'])
		stack = Stack.objects.get(pk=item.stack_id)
		stacks = Stack.objects.all()
		items_recent = Item.objects.all().order_by('-created_date')[0:5]
		items_popular = Item.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		form = ItemCommentForm(request.POST)
		item_comments = item.comments.all()
		item.number_comments = item_comments.count()
		item.number_views = item.number_views + 1
		item.save()
		return render(request, self.template, {
			'section': {
				'name': stack.name
			},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/library/' + stack.name.lower() + '/' + item.slug,
			'og_title': item.title,
			'og_description': item.description,
			'og_image': 'http://www.nonhumanuser.com' + item.image.url if item.image else '',
			'item': item,
			'stack': stack,
			'stacks': stacks,
			'items_recent': items_recent,
			'items_popular': items_popular,
			'links': links,
			'form': form,
			'comments': item_comments, 'icon_class': 'lg_icon_class_library'})


class ItemResourceView(View):
	"""Old /media/library/item/... links: redirect to the file in media storage."""
	def get(self, request, *args, **kwargs):
		name = 'library/item/{year}/{month}/{day}/{filename}'.format(**self.kwargs)
		return HttpResponseRedirect(default_storage.url(name))


class ItemCommentView(View):
	template = 'library/item.html'

	def post(self, request, *args, **kwargs):
		form = ItemCommentForm(request.POST)

		if form.is_valid():
			comment = form.cleaned_data['comment']
			user = request.user
			item = Item.objects.get(pk=request.POST.get('item_id'))
			instance = ItemComment(comment=comment, user=user, item=item)
			instance.save()

		return HttpResponseRedirect(
			'/library/' + kwargs['stack'] + '/' + kwargs['slug'] + '/')
	
	
class ItemArchiveView(View):
	template = 'library/library_list.html'

	def get(self, request, *args, **kwargs):
		items_recent = Item.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Item.objects.filter(active=True,
											publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		items = Item.objects.filter(active=True,
									publish_date__lte=datetime.datetime.now()).order_by('-created_date')
		stacks = Stack.objects.all()
		links = get_main_links()
		context = {
			'section': { 'name': 'Library' }
		}
		context['og_type'] = 'webpage'
		context['og_url'] = 'http://www.nonhumanuser.com/Items/article_archive/'
		context['og_title'] = 'Library Archive'
		context['og_description'] = 'Resources and content for the Call of Cthulhu role playing game.'
		context['og_image'] = 'http://www.nonhumanuser.com//images/Library.png'
		context['items_recent'] = items_recent
		context['items_popular'] = items_popular
		context['links'] = links
		context['icon_class'] = 'lg_icon_class_library'
		context['items'] = items
		context['stacks'] = stacks

		return render(request, self.template, context)