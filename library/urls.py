from django.conf.urls import url
from library.views import IndexView, ItemsView, ItemView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
	url(r'^(?P<slug>[\w-]+)/$', ItemsView.as_view(), name='items'),
	url(r'^(?P<stack>[\w-]+)/(?P<slug>[\w-]+)/$', ItemView.as_view(), name='item'),
]