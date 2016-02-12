from django.conf.urls import url
from library.views import IndexView

urlpatterns = [
	url(r'^$', IndexView.as_view(), name='index'),
]