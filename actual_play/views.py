from django.shortcuts import render
from django.views.generic import View
from actual_play.models import GameGroup, Game, Player
from nonhumanuser.utils import *

# Create your views here.
class IndexView(View):
	def get(self, request):
		groups = GameGroup.objects.all()
		items_recent = Game.objects.all().order_by('-created_date')[0:5]
		items_popular = Game.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, 'actual_play/index.html', {'section': 
			{'name': 'Actual Play'}, 'groups': groups, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class GameGroupView(View):
	template = 'actual_play/games.html'

	def get(self, request, *args, **kwargs):
		group = GameGroup.objects.get(slug=self.kwargs['slug'])
		games = Game.objects.filter(group=group.pk)
		items_recent = Game.objects.all().order_by('-created_date')[0:5]
		items_popular = Game.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': 'Actual Play'},
			'group': group, 'games': games, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class GameView(View):
	template = 'actual_play/game.html'

	def get(self, request, *args, **kwargs):
		print(kwargs)
		game = Game.objects.filter(slug=self.kwargs['slug'])
		items_recent = Game.objects.all().order_by('-created_date')[0:5]
		items_popular = Game.objects.all().order_by('-number_comments')[0:5]
		links = get_main_links()
		return render(request, self.template, {'section': {'name': 'Actual Play'},
			'game': game, 'items_recent': items_recent, 
			'items_popular': items_popular, 'links': links})


class GameResourceView(View):
	def get(self, request, *args, **kwargs):
		file_path = settings.MEDIA_ROOT + '/game/' + self.kwargs['type'] + '/' \
		+ self.kwargs['year'] + '/' + self.kwargs['month'] + '/' + self.kwargs['day'] + \
		'/' + self.kwargs['filename']
		file_wrapper = FileWrapper(open(file_path, 'rb'))
		file_mimetype = mimetypes.guess_type(file_path)
		response = HttpResponse(file_wrapper, content_type=file_mimetype)
		response['X-Sendfile'] = file_path
		response['Content-Length'] = os.stat(file_path).st_size
		response['Content-Diposition'] = 'attachment; filename=%s' % smart_str(self.kwargs['filename'])
		return response
