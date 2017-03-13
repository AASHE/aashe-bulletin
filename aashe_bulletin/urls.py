import django_membersuite_auth.urls
from django.conf.urls import patterns, include, url
from django.contrib import admin
from bulletin.tools.plugins.views.story import StoryListView

from views import (AllItemsView,
                   FAQView,
                   LatestNewsFeedView,
                   NoSearchForYouView,
                   SubmissionGuidelinesView)

admin.autodiscover()

urlpatterns = patterns(
    '',

    url(r'^$',
        StoryListView.as_view(),
        name='front-page'),

    url(r'^all-items/$',
        AllItemsView.as_view(),
        name='all-items'),

    url(r'^accounts/',
        include(django_membersuite_auth.urls)),

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

    url(r'^rss/news/$',
        LatestNewsFeedView(),
        name='latest-news-feed'),

    url(r'^rss/news/category/(?P<category>.+)/$',
        LatestNewsFeedView(),
        name='latest-news-category-feed'),

    url(r'^',
        include('bulletin.urls',
                namespace='bulletin')),
)
