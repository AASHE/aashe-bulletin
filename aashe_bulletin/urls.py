import aashe.aasheauth.urls
from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import BulletinHelpView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^newsletter/', include('bulletin.urls', namespace='bulletin')),

    url(r'^accounts/', include(aashe.aasheauth.urls)),

    url(r'^help/',
        BulletinHelpView.as_view(),
        name='help'),

    url(r'^admin/', include(admin.site.urls)),
)
