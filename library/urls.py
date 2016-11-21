from django.conf.urls import url
from library.views import IndexView, ItemsView, ItemView, ItemResourceView, ItemCommentView, ItemArchiveView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
    url(r'^library_archive/$', ItemArchiveView.as_view(), name="library-archive"),
	url(r'^(?P<slug>[\w-]+)/$', ItemsView.as_view(), name='library-items'),
	url(r'^(?P<stack>[\w-]+)/(?P<slug>[\w-]+)/$', ItemView.as_view(), 
    name='library-item'),
	url(r'^item/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$', 
		ItemResourceView.as_view(), name='resource'),
	url(r'^(?P<stack>[\w-]+)/(?P<slug>[\w-]+)/comment/$', 
    ItemCommentView.as_view(), name='comment'),
]