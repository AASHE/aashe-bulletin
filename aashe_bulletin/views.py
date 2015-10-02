from braces.views import SetHeadlineMixin
from django.core.urlresolvers import reverse
from django.views.generic import RedirectView, TemplateView

from bulletin import views as bulletin_views


class FrontPageView(bulletin_views.FrontPageView,
                    bulletin_views.SidebarView):

    template_name = 'bulletin/front_page.html'
    headline = 'All Items'


class FAQView(SetHeadlineMixin,
              bulletin_views.SidebarView,
              TemplateView):

    headline = 'Frequently Asked Questions'
    template_name = 'faq.html'


class NoSearchForYouView(TemplateView):

    template_name = 'no_search_for_you.html'


class SubmissionGuidelinesView(SetHeadlineMixin,
                               bulletin_views.SidebarView,
                               TemplateView):

    headline = 'Submission Guidelines'
    template_name = 'submission_guidelines.html'
