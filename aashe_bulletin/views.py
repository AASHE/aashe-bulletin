from braces.views import SetHeadlineMixin
from django.views.generic import TemplateView

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


class SubmissionGuidelinesView(SetHeadlineMixin,
                               bulletin_views.SidebarView,
                               TemplateView):

    headline = 'Submission Guidelines'
    template_name = 'submission_guidelines.html'
