from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^sucursales/$', 'microsip_consolidador.apps.config.sucursales.views.sucursales_view'),
    (r'^sucursal/(?P<id>\d+)/', 'microsip_consolidador.apps.config.sucursales.views.sucursal_manageview'),
    (r'^sucursal/', 'microsip_consolidador.apps.config.sucursales.views.sucursal_manageview'),
)