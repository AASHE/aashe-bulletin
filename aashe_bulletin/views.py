from braces.views import SetHeadlineMixin
from django.views.generic import TemplateView

from bulletin.views import SidebarView


class FAQView(SetHeadlineMixin,
                       SidebarView,
                       TemplateView):

    headline = 'Frequently Asked Questions'
    template_name = 'faq.html'


class SubmissionGuidelinesView(SetHeadlineMixin,
                               SidebarView,
                               TemplateView):

    headline = 'Submission Guidelines'
    template_name = 'submission_guidelines.html'
