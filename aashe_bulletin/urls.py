from django.conf.urls import patterns, include, url

import bulletin
from views import BulletinHelpView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'aashe_bulletin.views.home', name='home'),
    url(r'^newsletter/', include('bulletin.urls', namespace='bulletin')),

    url(r'^help/',
        BulletinHelpView.as_view(),
        name='help'),

    url(r'^admin/', include(admin.site.urls)),
)
