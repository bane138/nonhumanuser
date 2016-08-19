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
	library_item = Item.objects.filter(active=True).last()
	game = Game.objects.last()
	game_group = GameGroup.objects.filter(name=game.group).first()
	entry_recent = Entry.objects.filter(active=True).order_by('-created_date')
	library_recent = Item.objects.filter(active=True).order_by('-created_date')
	games_recent = Game.objects.filter(active=True).order_by('-created_date')
	items_recent = list(chain(entry_recent, library_recent, games_recent))
	entry_popular = Entry.objects.filter(active=True).order_by('-number_comments')
	
	items_popular = list(chain())
	context = {
		"site": { 
			"title": "NonHumanUser",
			"description": "Stories, articles resources and supplements for Call of Cthulhu and related genre games." 
		},
		'story': story,
		'article': article,
		'library_item': library_item,
		'game': game,
		'game_group': game_group,
		'items_recent': items_recent[0:5],
		'section': 'main',
	}
	return render(request, 'app/index.html', context)
