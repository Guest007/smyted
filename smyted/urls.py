# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from yammled.views import Home


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', Home.as_view(), name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^inplaceeditform/', include('inplaceeditform.urls')),
)

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += (static(settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT))


