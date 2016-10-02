from django.conf.urls import url
<<<<<<< HEAD
from actual_play.views import IndexView,GameGroupView,GameView,GameResourceView,GameCommentView
=======
from actual_play.views import IndexView,GameGroupView,\
GameView,GameResourceView,GameCommentView
>>>>>>> 2a5a7abc3ce316b9bf75a62408a01e1916372d5e

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<slug>[\w-]+)/$', GameGroupView.as_view(), name='game group'),
	url(r'^(?P<group>[\w-]+)/(?P<slug>[\w-]+)/$', GameView.as_view(), 
    name="game"),
  url(r'^audio/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$', 
    GameResourceView.as_view(), name='resource'),
  url(r'^video/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$',
    GameResourceView.as_view(), name='resource'),
  url(r'^(?P<group>[\w-]+)/(?P<slug>[\w-]+)/comment/$', 
    GameCommentView.as_view(), 
    name="comment"),
]