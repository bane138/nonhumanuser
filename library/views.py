from django.shortcuts import render
from django.views.generic import View
from library.models import Item, Stack

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
