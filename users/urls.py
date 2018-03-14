from django.conf.urls import url
from . import views

app_name = 'users'
urlpatterns = [
	url(r'^register/$', views.register, name='register'),
	url(r'^personal/$', views.personal, name='personal'),
	url(r'^collect_commodity/$', views.collect_commodity, name='collect_commodity'),
	url(r'^(?P<user>.+)/collentions/$', views.collentions, name='collentions'),
	url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_collention, name='delete_collention'),
]