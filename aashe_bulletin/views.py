from braces.views import SetHeadlineMixin
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from bulletin import views as bulletin_views
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

    title = 'AASHE Bulletin news'
    description = 'Latest news from the AASHE Bulletin.'

    def link(self):
        return reverse('latest-news-feed')

    def items(self):
        return Story.objects.filter(approved=True).order_by('-pub_date')[:5]

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
