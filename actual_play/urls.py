from django.conf.urls import url
from actual_play.views import IndexView, GameGroupView, GameView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<slug>[\w-]+)/$', GameGroupView.as_view(), name='game group'),
	url(r'^(?P<group>[\w-]+)/(?P<slug>[\w-]+)/$', GameView.as_view(), name="game"),
]