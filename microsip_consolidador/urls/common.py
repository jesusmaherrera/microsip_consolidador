from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import autocomplete_light
autocomplete_light.autodiscover()

urlpatterns = patterns('',
    #main
    url(r'', include('microsip_consolidador.apps.main.urls', namespace='main')),
    # url(r'autocomplete/', include('autocomplete_light.urls')),
  
    # #LOGIN
    url(r'^select_db/$','microsip_consolidador.apps.main.views.select_db'),    
    url(r'^login/$','microsip_consolidador.apps.main.views.ingresar'),
    url(r'^logout/$', 'microsip_consolidador.apps.main.views.logoutUser'),
)
 
urlpatterns += staticfiles_urlpatterns()