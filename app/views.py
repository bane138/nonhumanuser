from django.shortcuts import render
import datetime
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item

# Create your views here.
def index(request):
	story = Entry.objects.last()
	article= Entry.objects.last()
	library_item = Item.objects.last()
	game = Game.objects.last()
	game_group = GameGroup.objects.get(name=game.group)
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
	}
	return render(request, 'app/index.html', context)
