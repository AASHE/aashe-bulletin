from braces.views import SetHeadlineMixin
from django.views.generic import TemplateView

from bulletin.views import SidebarView


class BulletinHelpView(SetHeadlineMixin,
                       SidebarView,
                       TemplateView):

    headline = 'Help'
    template_name = 'bulletin_help.html'


class SubmissionGuidelinesView(SetHeadlineMixin,
                               SidebarView,
                               TemplateView):

    headline = 'Submission Guidelines'
    template_name = 'submission_guidelines.html'
