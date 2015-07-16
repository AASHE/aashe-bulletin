"""Load job data dumped from Drupal into Job objects.
"""
import csv
import datetime

from django.contrib.auth.models import User

from bulletin.models import Issue, Newsletter, Section
from bulletin.tools.plugins.models import Job


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
           'Nov': 11, 'Dec': 12}
    if str in map:
        return map[str]
    else:
        return int(str)


def str_to_date(str, date_type):
    """Return the date represented by `str`.
    """
    if date_type == 'post_date':
        # Jan 7 2014 - 5:19pm
        month_str, day_str, year_str = str.split('-')[0].split()
        return datetime.date(int(year_str),
                             int_for_month(str=month_str),
                             int(day_str))
    elif date_type == 'issue_date':
        try:
            # ['January', '14,', '2014']
            month_str, day_str, year_str = str[0], str[1], str[2]
        except IndexError:
            # ['M/DD/YY']
            month_str, day_str, year_str = str[0].split('/')
            return datetime.date(int(year_str),
                                 int(month_str),
                                 int(day_str))
    else:
        # January 2, 2014
        month_str, day_str, year_str = str.split()
        return datetime.date(int(year_str),
                             int_for_month(str=month_str),
                             int(day_str[:-1]))  # drop trailing comma on day


def job_factory(job_data, issue):
    """Create a job based on `job_data`.
    """
    # Get or create a Section.
    try:
        section = issue.sections.get(name='Jobs')
    except Section.DoesNotExist:
        section = Section.objects.create(name='Jobs',
                                         issue=issue)

    # job_data['title'] includes the organization, as the last
    # clause preceeded by a comma. We capture that in the Job.organization
    # field, so we chop it off the title here.
    title = ' '.join(job_data['title'].split(',')[:-1])

    institution = (job_data['institutions'] or
                   job_data['other_organizations'] or
                   job_data['title'].split(',')[-1])

    job = Job.objects.create(
        date_submitted=str_to_date(job_data['post_date'],
                                   'post_date'),
        title=title,
        url=job_data['url'],
        submitter=historian_account(),
        approved=True,
        include_in_newsletter=True,
        section=section,
        pub_date=issue.pub_date,
        organization=institution)

    return job


def name_issue(issue_date_str):
    # January 20, 2015 November 18, 1999
    # Only want first date, if there's more than one.
    try:
        # Jan. 7 2010
        month_str, day_str, year_str = issue_date_str.split()[:3]
    except ValueError:
        # M/DD/YY
        month_str, day_str, year_str = issue_date_str.split('/')
    return 'Bulletin {year}-{month}-{day}'.format(
        year=year_str,
        month=str(int_for_month(month_str)).zfill(2),
        day=day_str[:-1].zfill(2))


def main():
    """Loads CSV from Drupal into Job objects.  May also also create
    Category, Issue, and Section objects.
    """

    newsletter = Newsletter.objects.get(name="AASHE Bulletin")
    new_jobs = []  # Jobs created.

    skipped_no_issue_date = []  # Jobs skipped because no issue date.
    skipped_unpublished = []  # Jobs skipped because they're "unpublished".

    with open('dumps/jobs.csv') as csvfile:
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

            job_data = {'title': row[0],
                        'post_date': row[1],
                        'deadline': row[2],
                        'issue_date': row[3],
                        'institutions': row[4],
                        'other_organizations': row[5],
                        'url': row[6]}

            # Sometimes the issue date is blank. For now, we're
            # just counting and skipping these.
            if not job_data['issue_date']:
                skipped_no_issue_date.append(job_data)
                continue

            # Sometimes the issue date is "unpublished". We're just
            # counting and skipping these, too.
            if 'unpublished' in job_data['issue_date'].lower():
                skipped_unpublished.append(job_data)
                continue

            # What we're calling "issue_date" here is sometimes
            # a list of dates. When that happens, we only care about
            # the first one.
            pub_date = str_to_date(job_data['issue_date'].split()[:3],
                                   'issue_date')

            # Get or create an Issue.
            try:
                issue = Issue.objects.get(pub_date=pub_date)
            except Issue.DoesNotExist:
                issue_name = name_issue(job_data['issue_date'])
                issue = Issue.objects.create(
                    newsletter=newsletter,
                    name=issue_name,
                    pub_date=pub_date)

            unloadable = []

            try:
                new_job = job_factory(job_data, issue)
            except Exception as exc:
                unloadable.append(job_data)
                unloadable.append(exc)
            new_jobs.append(new_job)

    return {'new_jobs': new_jobs,
            'skipped_no_issue_date': skipped_no_issue_date,
            'skipped_unpublished': skipped_unpublished,
            'unloadable': unloadable}
