from django.conf.urls import url
from actual_play.views import IndexView,GameTypeView,\
GameView,GameResourceView,GameCommentView, GameArchiveView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^game_archive/$', GameArchiveView.as_view(), name="all-game-archive"),
    url(r'^game_archive/(?P<game_type>[\w-]+)/$', GameArchiveView.as_view(), name="game-archive"),
    url(r'^(?P<game_type>[\w-]+)/$', GameTypeView.as_view(), name='game-type'),
    url(r'^(?P<game_type>[\w-]+)/(?P<slug>[\w-]+)/$', GameView.as_view(),
    name="game"),
    url(r'^audio/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$',
    GameResourceView.as_view(), name='resource'),
    url(r'^video/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$',
    GameResourceView.as_view(), name='resource'),
    url(r'^(?P<type>[\w-]+)/(?P<slug>[\w-]+)/comment/$',
    GameCommentView.as_view(),
    name="comment"),
]
