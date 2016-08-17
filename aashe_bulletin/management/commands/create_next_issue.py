#!/usr/bin/env python
"""Creates new issue, with pub date of next Tuesday, then fills the
issue.
"""
import calendar
import datetime

from django.core.management.base import BaseCommand

from bulletin.api.views import IssueFill
from bulletin.models import Issue, IssueTemplate


class Command(BaseCommand):

    def handle(self, *args, **options):
        issue_template = IssueTemplate.objects.first()  # only 1 so far
        next_tuesday = get_next_tuesday()
        issue = create_issue(issue_template=issue_template,
                             pub_date=next_tuesday)
        fill_issue(issue)


def get_next_tuesday():
    today = datetime.date.today()
    next_tuesday = today + datetime.timedelta((calendar.TUESDAY -
                                               today.weekday()) % 7)
    return next_tuesday


def create_issue(issue_template, pub_date):
    name = pub_date.strftime("Bulletin %B %d, %Y")
    issue = Issue(newsletter=issue_template.newsletter,
                  name=name,
                  pub_date=pub_date)
    issue.init_from_issue_template(issue_template)
    issue.save()
    return issue


def fill_issue(issue):
    issue_fill_view = IssueFill(kwargs={"pk": issue.pk})
    issue_fill_view.fill_issue()
