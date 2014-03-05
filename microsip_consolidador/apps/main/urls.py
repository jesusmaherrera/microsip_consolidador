from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', 'microsip_consolidador.apps.main.views.index'),
)