from django.shortcuts import render
from django.views.generic import View
from library.models import Item

# Create your views here.
class IndexView(View):
	def get(self, request):
		items = Item.objects.all()
		return render(request, 'library/index.html', {'items': items})
