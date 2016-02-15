from django.shortcuts import render
import datetime
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item

# Create your views here.
def index(request):
	story = Entry.objects.filter(created_date__gte=datetime.date.today())
	article= Entry.objects.filter(created_date__gte=datetime.date.today())
	library_item = Item.objects.filter(created_date__gte=datetime.date.today())
	game = Game.objects.filter(created_date__gte=datetime.date.today())
	context = {
		"site": { 
			"title": "Non Human User",
			"description": "Stories, articles resources and supplements for Call of Cthulhu and related genre games." 
		},
		"story": story,
		"article": article,
		"library_item0": library_item,
		"game": game
	}
	return render(request, 'app/index.html', context)
