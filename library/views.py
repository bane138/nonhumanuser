from django.shortcuts import render
from django.views.generic import View
from library.models import Item, Stack
from nonhumanuser import settings
import os
import mimetypes
from django.http import HttpResponse
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str

# Create your views here.
class IndexView(View):
	def get(self, request):
		stacks = Stack.objects.all()
		return render(request, 'library/index.html', {'section': {'name': 'Library'}, 
			'stacks': stacks})


class ItemsView(View):
	template = 'library/items.html'

	def get(self, request, *args, **kwargs):
		stack = Stack.objects.get(slug=self.kwargs['slug'])
		items = Item.objects.filter(stack__exact=stack.id)
		return render(request, self.template, {'section': {'name': 'Library'}, 
			'items': items, 'stack': stack})


class ItemView(View):
	template = 'library/item.html'

	def get(self, request, *args, **kwargs):
		item = Item.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Library'}, 
			'item': item})


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