from django.urls import path, re_path
from actual_play.views import IndexView,GameTypeView,\
GameView,GameResourceView,GameCommentView, GameArchiveView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('game_archive/', GameArchiveView.as_view(), name="all-game-archive"),
    re_path(r'^game_archive/(?P<game_type>[\w-]+)/$', GameArchiveView.as_view(), name="game-archive"),
    re_path(r'^(?P<game_type>[\w-]+)/$', GameTypeView.as_view(), name='game-type'),
    re_path(r'^(?P<game_type>[\w-]+)/(?P<slug>[\w-]+)/$', GameView.as_view(),
    name="game"),
    re_path(r'^audio/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$',
    GameResourceView.as_view(), name='resource'),
    re_path(r'^video/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$',
    GameResourceView.as_view(), name='resource'),
    re_path(r'^(?P<type>[\w-]+)/(?P<slug>[\w-]+)/comment/$',
    GameCommentView.as_view(),
    name="comment"),
]
