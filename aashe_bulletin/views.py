from braces.views import SetHeadlineMixin
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.utils.http import urlunquote
from django.views.generic import TemplateView

from bulletin import views as bulletin_views
from bulletin.models import Category
from bulletin.tools.plugins.models import Story


class AllItemsView(bulletin_views.FrontPageView,
                   bulletin_views.SidebarView):

    template_name = 'all_items.html'
    headline = 'All Items'


class FAQView(SetHeadlineMixin,
              bulletin_views.SidebarView,
              TemplateView):

    headline = 'Frequently Asked Questions'
    template_name = 'faq.html'


class LatestNewsFeedView(Feed):

    def get_object(self, request, category=None):
        if category:
            return get_object_or_404(Category,
                                     name__iexact=urlunquote(category))
        return None

    def title(self, obj):
        if obj is not None:
            return 'AASHE Bulletin ' + obj.name + ' News'
        else:
            return 'AASHE Bulletin News'

    def description(self, obj):
        if obj is not None:
            return ('Latest ' + obj.name.lower() +
                    ' news from the AASHE Bulletin.')
        else:
            return 'Latest news from the AASHE Bulletin.'

    def link(self, obj):
        if obj is not None:
            return reverse('latest-news-category-feed',
                           kwargs={'category': obj.name})
        else:
            return reverse('latest-news-feed')

    def items(self, obj):
        qs = Story.objects.filter(approved=True).order_by('-pub_date')
        if obj is not None:
            qs = qs.filter(category=obj)
        return qs[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.blurb

    def item_link(self, item):
        return item.url


class NoSearchForYouView(TemplateView):

    template_name = 'no_search_for_you.html'


class SubmissionGuidelinesView(SetHeadlineMixin,
                               bulletin_views.SidebarView,
                               TemplateView):

    headline = 'Submission Guidelines'
    template_name = 'submission_guidelines.html'
