from django.conf.urls.defaults import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'crime.views.map'),
    url(r'^crimes$', 'crime.views.crimes'),
    url(r'^admin/', include(admin.site.urls)),
)
