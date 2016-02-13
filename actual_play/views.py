from django.shortcuts import render
from django.views.generic import View
from actual_play.models import GameGroup, Game, Player

# Create your views here.
class IndexView(View):
	def get(self, request):
		groups = GameGroup.objects.all()
		return render(request, 'actual_play/index.html', {'groups': groups})


class GameGroupView(View):
	template = 'actual_play/games.html'

	def get(self, request, *args, **kwargs):
		group = GameGroup.objects.get(slug=self.kwargs['slug'])
		games = Game.objects.filter(group__exact=group.id)
		return render(request, self.template, {'group': group, 'games': games})


class GameView(View):
	template = 'actual_play/game.html'

	def get(self, request, *args, **kwargs):
		game = Game.objects.get(slug=self.kwargs['slug'])
		return render(request, self.template, {'game': game})
