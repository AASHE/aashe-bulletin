"""Load event data dumped from Drupal into Event objects.
"""
import csv
import datetime

from django.contrib.auth.models import User

from apps.newsletter.models import Issue, Newsletter, Section
from apps.plugins.models import Event


def historian_account():
    """Return the Django account that will get credit for creating all
    these stories.
    """
    try:
        return User.objects.get(username='bulletin-historian')
    except User.DoesNotExist:
        return User.objects.create(username='bulletin-historian',
                                   is_staff=True)


def int_for_month(str):
    """Return the number of the month that corresponds to the string `str`.
    """
    map = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
           'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
           'October': 10, 'November': 11, 'December': 12,
           'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
           'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
           'Nov': 11, 'Dec': 12,
           'Sept': 9}
    return map[str]


def str_to_date(str, date_type):
    """Return the date represented by `str`.
    """
    if date_type == 'post_date':
        # Jan 7 2014 - 5:19pm
        #  or
        # 2013-12-11
        try:
            year_num_str, month_num_str, day_num_str = str.split('-')
        except ValueError:
            month_str, day_num_str, year_num_str = str.split('-')[0].split()
            month_num_str = int_for_month(str=month_str)
        return datetime.date(int(year_num_str),
                             int(month_num_str),
                             int(day_num_str))
    elif date_type == 'issue_date':
        # ['January', '14,', '2014']
        #  or
        # ['1/3/08']
        #  or
        # '01/22/2011 10/18/2011'

        # Try '01/22/2011 10/18/2011' first.
        try:
            date_string, _ = str.split()
        except AttributeError:
            # Try ['1/3/08'] next.
            try:
                month_num_str, day_num_str, year_num_str = str[0].split('/')
            except ValueError:
                month_str, day_str, year_num_str = str[0], str[1], str[2]
                if day_str[-1] == ',':
                    day_num_str = day_str[:-1]  # drop trailing comma on day
                month_num_str = int_for_month(str=month_str)
        else:
            month_num_str, day_num_str, year_num_str = date_string.split('/')

        return datetime.date(int(year_num_str),
                             int(month_num_str),
                             int(day_num_str))
    elif date_type == 'date_time':
        # Jan. 20, 2014
        #   or
        # May 20, 2014; 12:00 p.m. Eastern
        #   or
        # Jan. 20-25, 2014
        #  or
        # Feb. 28 - Mar. 1, 2014
        #  or
        # October 20
        #  or
        # March 23\xe2\x80\x9324, 2011
        #  or
        # May 28, 2013 at 2:00 p.m. ET
        #  or
        # Sept. 10, 2013: 11:30 a.m.

        # Drop the time.
        just_date = str.split(';')[0]

        if len(just_date.split()) < 3:
            just_date += ", 1000"  # These need to be addressed in db!!!

        # Split on 'at' if it's here:
        try:
            just_date = just_date.split('at')[0]
        except IndexError:
            pass

        # Split on ':' if it's here:
        try:
            just_date = just_date.split(':')[0]
        except IndexError:
            pass

        # Replace any pesky fancy dash:
        just_date = just_date.replace('\xe2\x80\x93', '-')

        try:
            month_str, day_str, year_str = just_date.split()
        except ValueError:  # Is it like 'Feb. 28 - Mar. 1, 2014'?
            start_date, end_date = just_date.split('-')
            month_str = start_date.split()[0]
            day_str = start_date.split()[1]
            year_str = end_date.split()[-1]

        # If the month is an abbreviation, lose the period.
        month_str = month_str.split('.')[0]

        # If the day ends with a comma, chop it off.
        day_str = day_str.replace(',', '')

        # Just use the starting day if it's a range.
        day_str = day_str.split('-')[0]

        return datetime.date(int(year_str),
                             int_for_month(str=month_str),
                             int(day_str))
    else:
        # January 2, 2014
        month_str, day_str, year_str = str.split()
        return datetime.date(int(year_str),
                             int_for_month(str=month_str),
                             int(day_str[:-1]))  # drop trailing comma on day


def event(event_data, issue):
    """Create a event based on `event_data`.
    """
    # Get or create a Section.
    try:
        section = issue.sections.get(name='Events')
    except Section.DoesNotExist:
        section = Section.objects.create(name='Events',
                                         issue=issue)

    institution = (event_data['institutions'] or
                   event_data['other_organizations'])

    event = Event.objects.create(
        date_submitted=str_to_date(event_data['post_date'],
                                   'post_date'),
        title=event_data['title'],
        url=event_data['url'],
        submitter=historian_account(),
        approved=True,
        include_in_newsletter=True,
        section=section,
        pub_date=issue.pub_date,
        organization=institution,
        location=institution,  # Because we have no real location.
        start_date=str_to_date(event_data['date_time'],
                               'date_time'))

    return event


def name_issue(issue_date_str):
    # 'January 20, 2015 November 18, 1999'
    # OR
    # '1/3/08'
    # OR
    # '01/24/2011 01/18/2011'

    # Do we have two slash-separated strings?
    try:
        d1, d2 = issue_date_str.split()
        if len(d1.split('/')) == 3:
            issue_date_str = d1
    except ValueError:
        pass

    # Is this a slash-separated string?
    try:
        month_num_str, day_num_str, year_num_str = issue_date_str.split('/')
    except ValueError:
        try:
            month_num_str, day_num_str, year_num_str = (
                issue_date_str.split()[0].split('/'))
        except ValueError:
            # Only want first date, if there's more than one.
            month_str, day_str, year_num_str = issue_date_str.split()[:3]
            day_num_str = day_str[:-1].zfill(2)
            month_num_str = str(int_for_month(month_str)).zfill(2)
        else:
            month_num_str = month_num_str.zfill(2)
            day_num_str = day_num_str.zfill(2)
            year_num_str = str(int(year_num_str) + 2000)
    return 'Bulletin {year}-{month}-{day}'.format(
        year=year_num_str,
        month=month_num_str,
        day=day_num_str)


def main():
    """Loads CSV from Drupal into Event objects.  May also also create
    Category, Issue, and Section objects.
    """

    newsletter = Newsletter.objects.get(name="AASHE Bulletin")
    new_events = []  # Events created.

    skipped_no_issue_date = []  # Events skipped because no issue date.
    skipped_unpublished = []  # Events skipped because they're "unpublished".
    skipped_global = []  # Skipped because global edition has no issue date.

    with open('bulletin/utils/dumps/bulletin_dump_events.csv') as csvfile:
        reader = csv.reader(csvfile)
        this_is_the_header = True
        for row in reader:
            # Kludge to skip the header row.
            if this_is_the_header:
                this_is_the_header = False
                continue

            # Skip empty rows.
            if not row:
                continue

            event_data = {'title': row[0],
                          'post_date': row[1],
                          'date_time': row[2],
                          'issue_date': row[3],
                          'institutions': row[4],
                          'other_organizations': row[5],
                          'url': row[6]}

            # Sometimes the issue date is blank. For now, we're
            # just counting and skipping these.
            if not event_data['issue_date']:
                skipped_no_issue_date.append(event_data)
                continue

            # Sometimes the issue date is "unpublished". We're just
            # counting and skipping these, too.
            if 'unpublished' in event_data['issue_date'].lower():
                skipped_unpublished.append(event_data)
                continue

            # Sometimes the issue date is something like "February
            # 2010 (Global)", and we can't parse a date from that,
            # so we're just counting and skipping these, too.
            try:
                if 'global' in event_data['issue_date'].split()[2].lower():
                    skipped_global.append(event_data)
                    continue
            except IndexError:
                pass

            # What we're calling "issue_date" here is sometimes
            # a list of dates. When that happens, we only care about
            # the first one.
            pub_date = str_to_date(event_data['issue_date'].split()[:3],
                                   'issue_date')

            # Get or create an Issue.
            try:
                issue = Issue.objects.get(pub_date=pub_date)
            except Issue.DoesNotExist:
                issue_name = name_issue(event_data['issue_date'])
                issue = Issue.objects.create(
                    newsletter=newsletter,
                    name=issue_name,
                    pub_date=pub_date)

            new_event = event(event_data, issue)
            new_events.append(new_event)

    return {'new_events': new_events,
            'skipped_no_issue_date': skipped_no_issue_date,
            'skipped_unpublished': skipped_unpublished,
            'skipped_global': skipped_global}
