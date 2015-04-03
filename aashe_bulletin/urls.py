import aashe.aasheauth.urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView

from views import FAQView, SubmissionGuidelinesView

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$',
        RedirectView.as_view(pattern_name='bulletin:plugins:story-list'),
        name='front-page'),

    url(r'^accounts/',
        include(aashe.aasheauth.urls)),

    url(r'^help/',
        FAQView.as_view(),
        name='faq'),

    url(r'^submission-guidelines/',
        SubmissionGuidelinesView.as_view(),
        name='submission-guidelines'),

    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^flat-pages/',
        include('django.contrib.flatpages.urls')),

    url(r'',
        include('bulletin.urls',
                namespace='bulletin')),
)
