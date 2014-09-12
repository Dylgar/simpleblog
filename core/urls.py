from django.conf import settings
from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('core.views',
    url(r'^$', 'index', {}),
	url(r'^add/$', 'add_entry'),
	url(r'^entry/([0-9]+)/edit/$', 'edit_entry'),
	url(r'^entry/([0-9]+)/$', 'entry'),
)


if settings.DEBUG:
    urlpatterns += patterns('django.views.generic.simple',
        url(r'^500/$', 'direct_to_template', {'template': '500.html'}),
        url(r'^404/$', 'direct_to_template', {'template': '404.html'}),
    )
