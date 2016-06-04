from django.shortcuts import render
import datetime
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item
from itertools import chain

# Create your views here.
def index(request):
	story = Entry.objects.last()
	article= Entry.objects.last()
	library_item = Item.objects.last()
	game = Game.objects.last()
	game_group = GameGroup.objects.get(name=game.group)
	entry_recent = Entry.objects.filter(active__exact=True)
	library_recent = Item.objects.filter(active__exact=True)
	games_recent = Game.objects.filter(active__exact=True)
	items_recent = list(chain(entry_recent, library_recent, games_recent))
	context = {
		"site": { 
			"title": "Non Human User",
			"description": "Stories, articles resources and supplements for Call of Cthulhu and related genre games." 
		},
		"story": story,
		"article": article,
		"library_item": library_item,
		"game": game,
		"game_group": game_group,
		"items_recent": games_recent #items_recent[0:5]
	}
	return render(request, 'app/index.html', context)
