# -*- coding: utf-8 -*-
"""For all extant issues, use 'ulysses.html' for the HTML template.

Previous templates expect one Category per Post; ulysses.html handles
multiple Categories per Post.

Since supporting multiple Categories per Post required a schema
change, historical HTML templates won't work even for historical Issues.
"""
from __future__ import unicode_literals

from django.db import migrations


def update_issues(apps, schema_editor):
    Issue = apps.get_model("bulletin", "Issue")
    for issue in Issue.objects.all():
        if issue.html_template_name:  # Many old Issues have no HTML template.
            issue.html_template_name = "email_templates/ulysses.html"
            issue.save()


class Migration(migrations.Migration):

    dependencies = [
        ("bulletin", "0005_delete_post_field_category")
    ]

    operations = [
        migrations.RunPython(update_issues)
    ]
