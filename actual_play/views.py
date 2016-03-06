from django.shortcuts import render
from django.views.generic import View
from actual_play.models import GameGroup, Game, Player

# Create your views here.
class IndexView(View):
	def get(self, request):
		groups = GameGroup.objects.all()
		return render(request, 'actual_play/index.html', {'section': {'name': 'Actual Play'}, 
			'groups': groups})


class GameGroupView(View):
	template = 'actual_play/games.html'

	def get(self, request, *args, **kwargs):
		group = GameGroup.objects.get(slug=self.kwargs['slug'])
		games = Game.objects.filter(group__exact=group.id)
		return render(request, self.template, {'section': {'name': 'Actual Play'},
			'group': group, 'games': games})


class GameView(View):
	template = 'actual_play/game.html'

	def get(self, request, *args, **kwargs):
		game = Game.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'section': {'name': 'Actual Play'},
			'game': game})


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
