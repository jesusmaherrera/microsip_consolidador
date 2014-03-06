from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^articulo_consolidado/(?P<clave>[a-zA-Z0-9_-]+)/', 'microsip_consolidador.apps.common.articulos.views.articulo_consolidado_view',),
)