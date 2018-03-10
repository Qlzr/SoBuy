from django.conf.urls import url
from . import views

app_name = 'search'
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^search/result/$', views.search_commodity, name='search_commodity'),
	url(r'^search/(?P<keyword>.+)/(?P<page>\d+)/$', views.search_page, name='search_page'),
]