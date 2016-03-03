# -*- coding: utf-8 -*-
"""Update default html_template_name in (the only) IssueTemplate.
"""
from __future__ import unicode_literals

from django.db import migrations


def update_issue_template(apps, schema_editor):
    IssueTemplate = apps.get_model("bulletin", "IssueTemplate")
    first_issue_template = IssueTemplate.objects.first()
    # make sure there's only one:
    last_issue_template = IssueTemplate.objects.first()
    assert first_issue_template == last_issue_template
    first_issue_template.html_template_name = "email_templates/victor.html"
    first_issue_template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aashe_bulletin', '0001_use_ulysses_for_historical_issues')
    ]

    operations = [
        migrations.RunPython(update_issue_template)
    ]
