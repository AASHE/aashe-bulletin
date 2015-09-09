import aashe.aasheauth.urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from views import (FAQView,
                   FrontPageView,
                   NoSearchForYouView,
                   SearchFirewallView,
                   SubmissionGuidelinesView)

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$',
        FrontPageView.as_view(),
        name='front-page'),

    url(r'^accounts/',
        include(aashe.aasheauth.urls)),

    url(r'^help/',
        FAQView.as_view(),
        name='faq'),

    url(r'^submission-guidelines/',
        SubmissionGuidelinesView.as_view(),
        name='submission-guidelines'),

    url(r'^search-firewall/',
        login_required(SearchFirewallView.as_view()),
        name='search-firewall'),

    url(r'^no-search-for-you/',
        NoSearchForYouView.as_view(),
        name='no-search-for-you'),

    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^flat-pages/',
        include('django.contrib.flatpages.urls')),

    url(r'^',
        include('bulletin.urls',
                namespace='bulletin')),
)
