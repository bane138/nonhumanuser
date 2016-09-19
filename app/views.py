from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from django.views.generic import View
from app.forms import UserForm, UserProfileForm
from actual_play.models import GameGroup, Game, Player
from blog.models import Blog, Entry, Category
from library.models import Stack, Item
from itertools import chain
from nonhumanuser.utils import *


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


def register(request):
	"""
	Register a user for the site :TODO NOT USED REMOVE
	"""
	context = RequestContext(request)

	# Boolean for weather the registration was successful or not
	registered = False

	# If POST we are handling form data
	if request.method == 'POST':
		# Grab information from the raw form
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If forms are valid
		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()

			# Hash password and save user
			user.set_password(user.password)
			user.save()

			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user

			# Do we have a profile picture?
			if 'avatar' in request.FILES:
				profile.avatar = request.FILES['avatar']

			profile.save()

			registered = True

		else:
			print(user_form.errors, profile_form.errors)

	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render_to_response(
		'app/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 
		'registered': registered, 'section': {'title': 'Register'}},
		context)


def user_login(request):
	"""
	Log user into site :TODO NOT USED REMOVE
	"""
	context = RequestContext(request)

	if request.method == 'POST':
		# Gather info
		username = request.POST['username']
		password = request.POST['password']

		# Authenticate
		user = authenticate(username=username, password=password)

		if user:
			# active?
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				# You are inactive, no soup for you
				return HttpResponse('Your account is disabled.')
		else:
			# Bad login
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse('Invalid login details supplied.')
	else:
		return render_to_response('app/login.html', {'section': {'title': 'Login'}}, context)


@login_required
def user_logout(request):
	"""
	:TODO NOT USED REMOVE
	"""
	# Log the user out
	logout(request)

	# Redirect to homepage
	return HttpResponseRedirect('/')


class ProfileView(View):
	"""
	Display user profile
	"""
	def get(self, request, *args, **kwargs):
		context = RequestContext(request)
		print(context)
		return render_to_response('app/profile.html', {'user': request.user}, 
			context)
