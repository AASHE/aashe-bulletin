from braces.views import SetHeadlineMixin
from django.views.generic import TemplateView

from bulletin.views import SidebarView


class BulletinHelpView(SetHeadlineMixin,
                       SidebarView,
                       TemplateView):

    headline = 'Help'
    template_name = "bulletin_help.html"
