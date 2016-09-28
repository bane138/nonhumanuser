from django.forms import ModelForm
from .models import Game, Player, GameComment

class GameCreateForm(ModelForm):
	class Meta:
		model = Game
		exclude = ('slug',)


class PlayerCreateForm(ModelForm):
	class Meta:
		model = Player
		exclude = ('slug',)


class GameCommentForm(ModelForm):
  class Meta:
    model = GameComment
    exclude = ('created_date', 'approved')