# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    url(r'^obj_create/(?P<mod_id>[a-zA-Z]+)/', 'yammled.views.obj_create'),
    url(r'^obj_update/(?P<mod_id>[a-zA-Z]+)/', 'yammled.views.obj_update'),
    url(r'^json_obj/(?P<mod_id>[a-zA-Z]+)/', 'yammled.views.json_obj'),
    url(r'^json_cls/', 'yammled.views.get_models_in_json'),
    url(r'^$', 'yammled.views.homepage'),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += (static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT))


