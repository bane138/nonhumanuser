from django.contrib import admin
from actual_play.models import GameGroup, GameType, GameEra, Game, Player, GameComment

# Register your models here.
class GameGroupAdmin(admin.ModelAdmin):
	pass


class GameTypeAdmin(admin.ModelAdmin):
	pass


class GameEraAdmin(admin.ModelAdmin):
	pass


class GameAdmin(admin.ModelAdmin):
	pass


class PlayerAdmin(admin.ModelAdmin):
	pass


class GameCommentAdmin(admin.ModelAdmin):
  pass


admin.site.register(GameGroup, GameGroupAdmin)
admin.site.register(GameType, GameTypeAdmin)
admin.site.register(GameEra, GameEraAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(GameComment, GameCommentAdmin)
