from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
	url(r'^$', 'sz.tmpviews.views.index', name='home'),
	url(r'^user-registration/$', 'sz.tmpviews.views.user_registration', name='user-registration'),

)