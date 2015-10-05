import aashe.aasheauth.urls
from django.conf.urls import patterns, include, url
from django.contrib import admin

from views import (FAQView,
                   FrontPageView,
                   LatestNewsFeedView,
                   NoSearchForYouView,
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

    url(r'^search-permission-denied/',
        NoSearchForYouView.as_view(),
        name='no-search-for-you'),

    url(r'^admin/',
        include(admin.site.urls)),

    url(r'^flat-pages/',
        include('django.contrib.flatpages.urls')),

    url(r'^rss/',
        LatestNewsFeedView(),
        name='latest-news-feed'),

    url(r'^',
        include('bulletin.urls',
                namespace='bulletin')),
)
