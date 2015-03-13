"""Load initial IssueTemplates (and SectionTemplates).
"""
from bulletin.models import (Category,
                             IssueTemplate,
                             Newsletter,
                             SectionTemplate)
from bulletin.tools.plugins.utils import get_active_plugins


def main():
    try:
        newsletter = Newsletter.objects.get(name='AASHE Bulletin')
    except Newsletter.DoesNotExist:
        newsletter = Newsletter.objects.create(
            name='AASHE Bulletin',
            mailing_list=('AASHE Bulletin (weekly news, '
                          'resources, opportunities and events)'))

    issue_template = IssueTemplate.objects.create(
        newsletter=newsletter,
        name='2015-01-26: 2 col',
        subject='',
        from_name='Crystal Simmons',
        from_email='bulletin@aashe.org',
        reply_to_email='bulletin@aashe.org',
        organization_name='AASHE',
        address_line_1='1536 Wynkoop St.',
        address_line_2='Suite 901',
        address_line_3='',
        city='Denver',
        state='CO',
        international_state='',
        postal_code='80202',
        country='US',
        html_template_name='v1.0.html',
        text_template_name='v1.0.txt')

    # Create a section for each type of Post. Include all Posts
    # of a type in those sections.

    name_to_section_name = {'story': 'News',
                            'event': 'Events',
                            'new resource': 'New Resources',
                            'opportunity': 'Opportunities',
                            'job': 'Jobs'}

    for plugin in get_active_plugins():

        section_template = SectionTemplate.objects.create(
            name=name_to_section_name[plugin.name],
            issue_template=issue_template)

        # Match all categories:
        for category in Category.objects.all():
            section_template.categories.add(category)

        section_template.content_types.add(plugin)

        section_template.save()
