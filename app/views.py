from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.views.generic import View, UpdateView
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item
from itertools import chain
from nonhumanuser.utils import *
from app.models import UserProfile


# Create your views here.
class IndexView(View):

	def get(self, request, *args, **kwargs):
		story = Entry.objects.filter(category=1).last()
		article= Entry.objects.filter(category=2).last()
		library_item = Item.objects.filter(active=True).last()
		game = Game.objects.last()
		game_group = GameGroup.objects.filter(name=game.group).first()
		entry_recent = Entry.objects.filter(active=True).order_by('-created_date')
		library_recent = Item.objects.filter(active=True).order_by('-created_date')
		games_recent = Game.objects.filter(active=True).order_by('-created_date')
		items_recent = list(chain(entry_recent, library_recent, games_recent))
		entry_popular = Entry.objects.filter(active=True).order_by('-number_comments')
		library_popular = Item.objects.filter(active=True).order_by('-number_comments')
		games_popular = Game.objects.filter(active=True).order_by('-number_comments')
		items_popular = list(chain(entry_popular, library_popular, games_popular))
		links = get_main_links()

		context = {
			"site": { 
				'title': 'NonHumanUser',
				'description': 'Stories, articles resources and supplements for Call of Cthulhu and related genre games.',
			},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com',
			'og_title': 'NonHumanUser',
			'og_description': 'Stories, articles resources and supplements for Call of Cthulhu and related genre games.',
			'og_image': 'http://www.nonhumanuser.com/images/logo.png',
			'story': story,
			'article': article,
			'library_item': library_item,
			'game': game,
			'game_group': game_group,
			'items_recent': items_recent[0:5],
			'items_popular': items_popular[0:5],
			'section': 'main',
			'links': links,
		}
		return render(request, 'app/index.html', context)


class ProfileView(UpdateView):
	"""
	Display user profile
	"""
	model = UserProfile
	fields = ['first_name', 'last_name', 'avatar']
	template_name = 'app/profile.html'
	slug_field = 'user_id'
	slug_url_kwarg = 'slug'

	"""
	def get(self, request, *args, **kwargs):
		context = RequestContext(request)
		return render_to_response('app/profile.html', {'user': request.user}, 
			context)
"""
