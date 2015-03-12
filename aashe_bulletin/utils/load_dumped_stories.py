import csv
import datetime

from django.contrib.auth.models import User

from apps.newsletter.models import Category, Issue, Newsletter, Section
from apps.plugins.models import Opportunity, NewResource, Story


def historian_account():
    """Return the Django account that will get credit for creating all
    these stories.
    """
    try:
        return User.objects.get(username='bulletin-historian')
    except User.DoesNotExist:
        return User.objects.create(username='bulletin-historian',
                                   is_staff=True)


def new_category_for(old_category_name):
    """Return the "new" category that's replaced the "old" category
    named `old_category`.
    """
    old_to_new_names = {
        'Education & Research': 'Academics',
        'Curriculum': 'Curriculum',
        'Co-Curricular Education & Student Organizing': 'Campus Engagement',
        'Research': 'Research',
        'Campus Operations': 'Operations',
        'Buildings': 'Buildings',
        'Climate': 'Air & Climate',
        'Dining Services': 'Dining Services',
        'Energy': 'Energy',
        'Grounds': 'Grounds',
        'Purchasing': 'Purchasing',
        'Transportation': 'Transportation',
        'Waste': 'Waste',
        'Water': 'Water',
        'Planning, Administration & Engagement': 'Planning & Administration',
        'Affordability & Access': 'Diversity & Affordability',
        'Assessments & Ratings': '',
        'Coordination & Planning': 'Coordination, Planning & Governance',
        'Diversity & Inclusion': 'Diversity & Affordability',
        'Health & Wellness': 'Health, Wellbeing & Work',
        'Human Resources': 'Health, Wellbeing & Work',
        'Investment': 'Investment',
        'Policy & Legislation': '',
        'Public Engagement': 'Public Engagement',
        'Other': 'Other',
        'Assessments & Ratings': 'Assessments & Ratings',
        'Funding': 'Funding',
        'Campus Sustainability in the Media':
        'Campus Sustainability in the Media',
        'Policy & Legislation': 'Policy & Legislation',
        'Other News': 'Other',
        '': 'Other',
        'Events': 'Other'
    }
    return Category.objects.get(name=old_to_new_names[old_category_name])


def int_for_month(str):
    """Return the number of the month that corresponds to the string `str`.
    """
    map = {'January': 1, 'February': 2, 'March': 3, 'April': 4,
           'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9,
           'October': 10, 'November': 11, 'December': 12,
           'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5,
           'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10,
           'Nov': 11, 'Dec': 12}
    return map[str]


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
    else:
        # January 2, 2014
        month_str, day_str, year_str = str.split()
        return datetime.date(int(year_str),
                             int_for_month(str=month_str),
                             int(day_str[:-1]))  # drop trailing comma on day


def story_to_opportunity(story_data, issue):
    """Create an Opportunity based on `story_data`.
    """
    # Get or create a Section.
    try:
        section = issue.sections.get(name='Opportunities')
    except Section.DoesNotExist:
        section = Section.objects.create(name='Opportunities',
                                         issue=issue)

    opportunity = Opportunity.objects.create(
        date_submitted=str_to_date(story_data['post_date'],
                                   'post_date'),
        title=story_data['title'],
        url=story_data['url'],
        submitter=historian_account(),
        approved=True,
        include_in_newsletter=True,
        section=section,
        blurb=story_data['body'],
        pub_date=issue.pub_date)

    return opportunity


def story_to_new_resource(story_data, issue):
    """Create a NewResource based on `story_data`.
    """
    # Get or create a Section.
    try:
        section = issue.sections.get(name='New Resources')
    except Section.DoesNotExist:
        section = Section.objects.create(name='New Resources',
                                         issue=issue)

    new_resource = NewResource.objects.create(
        date_submitted=str_to_date(story_data['post_date'],
                                   'post_date'),
        title=story_data['title'],
        url=story_data['url'],
        submitter=historian_account(),
        approved=True,
        include_in_newsletter=True,
        section=section,
        blurb=story_data['body'],
        pub_date=issue.pub_date)

    return new_resource


def story(story_data, issue):
    """Create a Story based on `story_data`.
    """
    # Get or create a Section.
    try:
        section = issue.sections.get(name='News')
    except Section.DoesNotExist:
        section = Section.objects.create(name='News',
                                         issue=issue)

    new_category = new_category_for(
        old_category_name=story_data['category_name'])

    story = Story.objects.create(
        date_submitted=str_to_date(story_data['post_date'],
                                   'post_date'),
        title=story_data['title'],
        url=story_data['url'],
        submitter=historian_account(),
        approved=True,
        include_in_newsletter=True,
        section=section,
        category=new_category,
        blurb=story_data['body'],
        date=str_to_date(story_data['story_date'],
                         'story_date'),
        pub_date=issue.pub_date)

    return story


def name_issue(issue_date_str):
    # 'January 20, 2015 November 18, 1999'
    # OR
    # '1/3/08'
    # Is this a slash-separated string?
    try:
        month_num_str, day_num_str, year_num_str = issue_date_str.split('/')
        month_num_str = month_num_str.zfill(2)
        day_num_str = day_num_str.zfill(2)
        year_num_str = str(int(year_num_str) + 2000)
    except ValueError:
        # Only want first date, if there's more than one.
        month_str, day_str, year_num_str = issue_date_str.split()[:3]
        day_num_str = day_str[:-1].zfill(2)
        month_num_str = str(int_for_month(month_str)).zfill(2)
    return 'Bulletin {year}-{month}-{day}'.format(
        year=year_num_str,
        month=month_num_str,
        day=day_num_str)


def main():
    """Loads CSV from Drupal into tables Story, NewResource, and
    Opportunity. Likely will also create records in Category, Issue,
    and Section.
    """

    newsletter = Newsletter.objects.get(name="AASHE Bulletin")
    new_stories = []  # Stories created.
    new_opportunities = []  # Opportunties created.
    new_new_resources = []  # NewResources created.

    skipped_bad_story_format = []  # Stories w/fundamentally bad data.
    skipped_no_issue_date = []  # Stories skipped because no issue date.
    skipped_unpublished = []  # Stories skipped because they're "unpublished".
    skipped_global = []  # Skipped because global edition has no issue date.

    with open('bulletin/utils/dumps/bulletin_dump_stories.csv') as csvfile:
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

            try:
                story_data = {'title': row[0],
                              'post_date': row[1],
                              'issue_date': row[2],
                              'institutions': row[3],
                              'other_organizations': row[4],
                              'story_date': row[5],
                              'url': row[6],
                              'body': row[7],
                              'category_name': row[8]}
            except IndexError:
                skipped_bad_story_format.append(story_data)
                continue

            # Sometimes the issue date is blank. For now, we're
            # just counting and skipping these.
            if not story_data['issue_date']:
                skipped_no_issue_date.append(story_data)
                continue

            # Sometimes the issue date is "unpublished". We're just
            # counting and skipping these, too.
            if 'unpublished' in story_data['issue_date'].lower():
                skipped_unpublished.append(story_data)
                continue

            # Sometimes the issue date is something like "February
            # 2010 (Global)", and we can't parse a date from that,
            # so we're just counting and skipping these, too.
            try:
                if 'global' in story_data['issue_date'].split()[2].lower():
                    skipped_global.append(story_data)
                    continue
            except IndexError:
                pass

            # What we're calling "issue_date" here is sometimes
            # a list of dates. When that happens, we only care about
            # the first one.
            pub_date = str_to_date(story_data['issue_date'].split()[:3],
                                   'issue_date')

            # Get or create an Issue.
            try:
                issue = Issue.objects.get(pub_date=pub_date)
            except Issue.DoesNotExist:
                issue_name = name_issue(story_data['issue_date'])
                issue = Issue.objects.create(
                    newsletter=newsletter,
                    name=issue_name,
                    pub_date=pub_date)

            # New Resources and Opportunities are a type of Story, but
            # in the new system they're a new type of content. They're
            # identified in this CSV by their category name of "New
            # Resources" or "Opportunities".
            if story_data['category_name'] == 'New Resources':
                new_new_resource = story_to_new_resource(story_data, issue)
                new_new_resources.append(new_new_resource)
            elif story_data['category_name'] == 'Opportunities':
                new_opportunity = story_to_opportunity(story_data, issue)
                new_opportunities.append(new_opportunity)
            else:
                new_story = story(story_data, issue)
                new_stories.append(new_story)

    return {'new_stories': new_stories,
            'new_opportunities': new_opportunities,
            'new_new_resources': new_new_resources,
            'skipped_no_issue_date': skipped_no_issue_date,
            'skipped_bad_story_format': skipped_bad_story_format,
            'skipped_unpublished': skipped_unpublished,
            'skipped_global': skipped_global}
