#!/usr/bin/env python
"""Truncates bulletin db by removing all Issues and Posts published more
than X months ago.

Note all months are, for our purposes here, 30 days long.
"""
import datetime
import uuid

from django.core.management.base import BaseCommand

from bulletin.models import Issue


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('-k', '--months-to-keep',
                            type=int,
                            metavar='months',
                            default=3,
                            help='delete data older than this many months')

    def handle(self, *args, **options):
        months_to_keep = options['months_to_keep']
        if get_confirmation(months_to_keep):
            print "Truncating ... "
            today = datetime.date.today()
            cutoff = today - datetime.timedelta(30 * months_to_keep)
            print "Deleting issues published before {} ...".format(cutoff)
            issue_qs = Issue.objects.filter(pub_date__lt=cutoff).reverse()
            for issue in issue_qs.all().prefetch_related('sections'):
                print 'Deleting issue published on {} ...'.format(
                    issue.pub_date)
                for section in issue.sections.all().prefetch_related('posts'):
                    section.posts.all().delete()
                issue.sections.all().delete()
            issue_qs.all().delete()
        else:
            print "Truncation cancelled."


def get_confirmation(months_to_keep):
    print "WARNING: You have begun a very destructive action."
    print ("WARNING: If you continue, much of the bulletin database will be "
           "destroyed.")
    print ("WARNING: Only the {} most recent months of data will "
           "remain.").format(months_to_keep)

    this_uuid = uuid.uuid4()
    print "TO CONTINUE, enter the following UUID:", this_uuid

    input_uuid = raw_input()

    return str(this_uuid) == input_uuid
