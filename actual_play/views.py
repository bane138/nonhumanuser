from django.shortcuts import render
from django.views.generic import View, ListView
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from actual_play.models import GameGroup, Game, Player, GameComment
from actual_play.forms import GameCommentForm
from nonhumanuser.utils import *
from nonhumanuser import settings
from wsgiref.util import FileWrapper
from django.utils.encoding import smart_str
from actual_play.models import GameComment
import mimetypes
import datetime
import os

# Create your views here.
class IndexView(View):
	def get(self, request):
		groups = GameGroup.objects.filter(active=True)
		items_recent = Game.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Game.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, 'actual_play/index.html', {'section': 
			{'name': 'Actual Play'},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/actual_play/',
			'og_title': 'Actual Plays',
			'og_description': 'Call of Cthulhu play sessions',
			'og_image': 'http://www.nonhumanuser.com/images/Actual_Play.png',
			'groups': groups,
			'items_recent': items_recent,
			'items_popular': items_popular,
			'links': links})


class GameGroupView(View):
	template = 'actual_play/games.html'

	def get(self, request, *args, **kwargs)
		group = GameGroup.objects.get(slug=self.kwargs['slug'])
		games_total = Game.objects.all()
		games = Game.objects.filter(group=group.pk, active=True, 
			publish_date__lte=datetime.datetime.now()).order_by('-publish_date')[0:5]
		items_recent = Game.objects.filter(group=group.pk, active=True, publish_date__lte=datetime.datetime.now())\
		.order_by('-created_date')[0:5]
		items_popular = Game.objects.filter(group=group.pk, active=True, publish_date__lte=datetime.datetime.now())\
		.order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {
			'section': {
				'name': 'Actual Play'
			},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/actual_play/' + group.slug + '/',
			'og_title': group.name,
			'og_description': group.status,
			'og_image': '',
			'group': group,
			'games': games,
			'items_recent': items_recent,
			'items_popular': items_popular,
			'links': links,
			'count': games_total.count(),
			'icon_class': 'lg_icon_class_actual_play'})


class GameView(View):
	template = 'actual_play/game.html'

	def get(self, request, *args, **kwargs):
		game = Game.objects.filter(slug=self.kwargs['slug']).first()
		group = game.group
		items_recent = Game.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Game.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		links = get_main_links()
		form = GameCommentForm(request.POST)
		game_comments = game.comments.all()
		game.number_comments = game_comments.count()
		game.number_views = game.number_views + 1
		game.save()
		return render(request, self.template, {
			'section': {
				'name': 'Actual Play'
			},
			'og_type': 'webpage',
			'og_url': 'http://www.nonhumanuser.com/actual_play/' + group.slug + '/' + game.slug,
			'og_title': game.title,
			'og_description': game.description,
			'og_image': 'http://www.nonhumanuser.com' + game.image.url if game.image else '',
			'game': game,
			'items_recent': items_recent,
			'items_popular': items_popular,
			'links': links,
			'form': form,
			'comments': game_comments, 'icon_class': 'lg_icon_class_actual_play'})


class GameResourceView(View):
	def get(self, request, *args, **kwargs):
		if 'mp3' in self.kwargs['filename'] or 'ogg' in self.kwargs['filename']:
			_type = 'audio/'
		else:
			_type = 'video/'

		file_path = settings.MEDIA_ROOT + '/actual_play/' + _type + '/' \
		+ self.kwargs['year'] + '/' + self.kwargs['month'] + '/'\
		 + self.kwargs['day'] + \
		'/' + self.kwargs['filename']
		file_wrapper = FileWrapper(open(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Diposition'] = 'attachment; filename=%s'\
		 % smart_str(self.kwargs['filename'])
		return response


class GameCommentView(View):
	template = 'actual_play/game.html'

	def post(self, request, *args, **kwargs):
		form = GameCommentForm(request.POST)

		if form.is_valid():
			comment = form.cleaned_data['comment']
			user = request.user
			game = Game.objects.get(pk=request.POST.get('game_id'))
			group = game.group
			instance = GameComment(comment=comment, game=game, user=user)
			instance.save()

		return HttpResponseRedirect(
			'/actual_play/' + kwargs['group'] + '/' + kwargs['slug'] + '/')


class GameArchiveView(View):
	template = 'actual_play/game_list.html'

	def get(self, request, *args, **kwargs):
		items_recent = Game.objects.filter(active=True,
										   publish_date__lte=datetime.datetime.now()).order_by('-created_date')[0:5]
		items_popular = Game.objects.filter(active=True,
											publish_date__lte=datetime.datetime.now()).order_by('-number_comments')[0:5]
		game_groups = GameGroup.objects.filter(active=True)
		games = Game.objects.filter(active=True, publish_date__lte=datetime.datetime.now()).order_by('-created_date')
		links = get_main_links()
		context = {
			'section': { 'name': 'Actual Play' }
		}
		context['og_type'] = 'webpage'
		context['og_url'] = 'http://www.nonhumanuser.com/actual_play/game_archive/'
		context['og_title'] = 'Game Archive'
		context['og_description'] = 'Recorded actual play sessions of Call of Cthulhu and Delta Green.'
		context['og_image'] = 'http://www.nonhumanuser.com//images/Actual_Play.png'
		context['items_recent'] = items_recent
		context['items_popular'] = items_popular
		context['links'] = links
		context['icon_class'] = 'lg_icon_class_actual_play'
		context['game_groups'] = game_groups
		context['games'] = games

		return render(request, self.template, context)