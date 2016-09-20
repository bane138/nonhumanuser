from django.shortcuts import render
from django.views.generic import View
from library.models import Item, Stack
from nonhumanuser import settings
import os
import mimetypes
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from nonhumanuser.utils import *
import datetime

# Create your views here.
class IndexView(View):
	def get(self, request):
		stacks = Stack.objects.all()
		items_recent = Item.objects.all().order_by('-created_date')[0:5]
		items_popular = Item.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, 'library/index.html', {'section': {'name': 'Library'}, 
			'stacks': stacks, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class ItemsView(View):
	template = 'library/items.html'

	def get(self, request, *args, **kwargs):
		stack = Stack.objects.get(slug=self.kwargs['slug'])
		stacks = Stack.objects.all()
		items = Item.objects.filter(stack__exact=stack.id, active=True, 
			publish_date__lte=datetime.datetime.now())[0:5]
		items_recent = Item.objects.all().order_by('-created_date')[0:5]
		items_popular = Item.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': stack.name}, 
			'items': items, 'stacks': stacks, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class ItemView(View):
	template = 'library/item.html'

	def get(self, request, *args, **kwargs):
		item = Item.objects.get(slug=self.kwargs['slug'])
		stack = Stack.objects.get(pk=item.stack_id)
		stacks = Stack.objects.all()
		items_recent = Item.objects.all().order_by('-created_date')[0:5]
		items_popular = Item.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': stack.name}, 
			'item': item, 'stacks': stacks, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class ItemResourceView(View):
	def get(self, request, *args, **kwargs):
		file_path = settings.MEDIA_ROOT + '/library/item/' + self.kwargs['year'] + \
		'/' + self.kwargs['month'] + '/' + self.kwargs['day'] + '/' + self.kwargs['filename']
		file_wrapper = FileWrapper(open(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Diposition'] = 'attachment; filename=%s' % smart_str(self.kwargs['filename'])
		return response


class ItemCommentView(View):
	def post(self, request, *args, **kwargs):
		pass