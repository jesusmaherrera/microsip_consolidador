from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    #main
    url(r'', include('microsip_consolidador.apps.main.urls', namespace='main')),
    url(r'', include('microsip_api.apps.config.urls', namespace='config')),
    # url(r'autocomplete/', include('autocomplete_light.urls')),
)
 
urlpatterns += staticfiles_urlpatterns()