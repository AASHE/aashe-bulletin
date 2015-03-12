"""
<p class="contentstarsheading">Education & Research
  <p class="subcategory">Co-Curricular Education & Student Organizing
    <table class="contenttable">
      <a class="contentlink"
         target="_blank"
         href="http://inside.iup...">
        Indiana U Purdue U Indianapolis Repurposes Food Waste
      </a>
    </table>
    <p class="contentbody">
      The university&rsquo;s new student-led food rescue and
      distribution operation will turn wasted food into meals for
      those in need while creating opportunities for student ...
      <a class="seealso" target="_blank"
         href="http://www.aashe.org/resources/co-curricular-education-resources/">
        AASHE Resource: Sustainability in Co-Curricular Education
      </a>
"""
from bs4 import BeautifulSoup
import datetime
import requests

from django.contrib.auth.models import User

from apps.newsletter.models import Category, Link
from apps.plugins.models import Story


BULLETIN_CLASSES = ('contentstarsheading',
                    'subcategory',
                    'contentlink',
                    'contentbody',
                    'seealso')

SUBMITTER = User.objects.get(username='admin')


def filter(tag):
    classes = tag.attrs.get('class', False)
    if classes:
        class_set = set(classes)
        bulletin_class_set = set(BULLETIN_CLASSES)
        return class_set.intersection(bulletin_class_set)
    return False


class BulletinStory(object):

    def __init__(self):
        self.stars_heading = ''
        self.subcategory = ''
        self.content_body = ''
        self.content_link = ''
        self.supplemental_links = []

    def copy_to_story(self):
        """Copies self into a plugins.models.Story.
        """
        story = Story()
        story.title = self.content_link['text']
        story.blurb = self.content_body
        story.url = self.content_link['url']

        # hardcoded stuff:
        story.date = datetime.date.today()
        story.approved = True
        story.submitter = SUBMITTER

        if stars_heading and self.subcategory:
            match_candidate = '/'.join([stars_heading,
                                        self.subcategory]).strip()
        else:
            match_candidate = stars_heading

        try:
            category = Category.objects.get(
                fully_qualified_name=match_candidate)
        except:
            print 'no Category for', match_candidate
        else:
            story.category = category

        story.save()

        print 'created story:', story

        # supplemental links:
        for link in self.supplemental_links:
            new_link = Link.objects.create(post=story,
                                           url=link['url'],
                                           text=link['text'])
            print 'created link:', new_link

        return


def load(month, day, year):
    """Load the bulletin published on the date indicated.

    Args should be integers.
    """
    req = requests.get(
        'http://www2.aashe.org/archives/'
        '{year}/{month}{day}.php'.format(
            year=year,
            month=str(month).zfill(2),
            day=str(day).zfill(2)))

    req.raise_for_status()

    html = BeautifulSoup(req.text)
    story = BulletinStory()
    for tag in html.find_all(filter):
        class_ = tag.attrs['class'][0]
        if class_ in ('contentstarsheading',
                      'subcategory'):
            if story.content_body:
                story.copy_to_story()
                story = BulletinStory()
        handlers[class_](tag, story)
    # last one
    story.copy_to_story()


def load_september():
    """Loads all stories from bulletins published in September.
    """
    for day in 9, 16, 23, 30:
        load(9, day, 2014)


def load_a_couple_years():
    for month in [m + 1 for m in xrange(12)]:
        for day in [d + 1 for d in xrange(31)]:
            for year in [2013, 2014]:
                try:
                    load(month, day, year)
                except requests.HTTPError:
                    pass

stars_heading = ''


def handle_contentstarsheading(tag, story):
    global stars_heading
    stars_heading = tag.text.strip()


def handle_subcategory(tag, story):
    story.subcategory = tag.text


def handle_contentlink(tag, story):
    story.content_link = {
        'url': tag.attrs['href'],
        'text': tag.text
    }


def handle_contentbody(tag, story):
    story.content_body = tag.text.split('See also:')[0]


def handle_seealso(tag, story):
    story.supplemental_links.append({
        'url': tag.attrs['href'],
        'text': tag.text
    })


handlers = {'contentstarsheading': handle_contentstarsheading,
            'subcategory': handle_subcategory,
            'contentlink': handle_contentlink,
            'contentbody': handle_contentbody,
            'seealso': handle_seealso}
