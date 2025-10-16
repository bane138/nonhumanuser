from django.urls import path, re_path
from library.views import IndexView, ItemsView, ItemView, ItemResourceView, ItemCommentView, ItemArchiveView

urlpatterns = [
	path('', IndexView.as_view(), name='index'),
    path('library_archive/', ItemArchiveView.as_view(), name="library-archive"),
	re_path(r'^(?P<slug>[\w-]+)/$', ItemsView.as_view(), name='library-items'),
	re_path(r'^(?P<stack>[\w-]+)/(?P<slug>[\w-]+)/$', ItemView.as_view(), 
    name='library-item'),
	re_path(r'^item/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<filename>[\w_\.]+)$', 
		ItemResourceView.as_view(), name='resource'),
	re_path(r'^(?P<stack>[\w-]+)/(?P<slug>[\w-]+)/comment/$', 
    ItemCommentView.as_view(), name='comment'),
]