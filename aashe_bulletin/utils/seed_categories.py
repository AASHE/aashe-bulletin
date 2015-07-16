from bulletin.models import Category

categories = {
    'Academics': [
        {'name': 'Curriculum',
         'url': 'http://www.aashe.org/resources/curriculum-resources/'},
        {'name': 'Research',
         'url': ('http://www.aashe.org/resources/'
                 'resources-sustainability-research/')},
    ],
    'Engagement': [
        {'name': 'Campus Engagement',
         'url': ('http://www.aashe.org/resources/'
                 'co-curricular-education-resources/')},
        {'name': 'Public Engagement',
         'url': ('http://www.aashe.org/resources/'
                 'resources-campus-public-engagement-sustainability/')},
    ],
    'Operations': [
        {'name': 'Air & Climate',
         'url': 'http://www.aashe.org/resources/climate-resources/'},
        {'name': 'Buildings',
         'url': ('http://www.aashe.org/resources/'
                 'green-buildings-higher-education/')},
        {'name': 'Dining Services',
         'url': 'http://www.aashe.org/resources/dining-services/'},
        {'name': 'Energy',
         'url': 'http://www.aashe.org/resources/resources-energy-management/'},
        {'name': 'Grounds',
         'url': 'http://www.aashe.org/resources/grounds/'},
        {'name': 'Purchasing',
         'url': 'http://www.aashe.org/resources/'
         'resources-sustainable-purchasing-higher-education/'},
        {'name': 'Transportation',
         'url': 'http://www.aashe.org/resources/'
         'resources-about-sustainable-transportation-campus/'},
        {'name': 'Waste',
         'url': 'http://www.aashe.org/resources/'
         'resources-waste-minimization-and-recycling-campus/'},
        {'name': 'Water',
         'url': 'http://www.aashe.org/resources/water-resources/'},
    ],
    'Planning & Administration': [
        {'name': 'Coordination, Planning & Governance',
         'url': 'http://www.aashe.org/resources/'
         'resources-sustainability-coordination-planning/'},
        {'name': 'Diversity & Affordability',
         'url': 'http://www.aashe.org/resources/'
         'resources-higher-education-affordability-and-access/'},
        {'name': 'Health, Wellbeing & Work',
         'url': 'http://www.aashe.org/resources/human-resources/'},
        {'name': 'Investment',
         'url': 'http://www.aashe.org/resources/'
         'resources-sustainable-investment-and-financing/'},
    ],
    'Innovation': [
        {'name': 'Innovation',
         'url': ''},
    ],
    'Other': [
        {'name': 'Assessments & Ratings',
         'url': ('http://www.aashe.org/resources/'
                 'assessment-tools-reports-indicators/')},
        {'name': 'Funding',
         'url': ''},
        {'name': 'Campus Sustainability in the Media',
         'url': ''},
        {'name': 'Policy & Legislation',
         'url': ('http://www.aashe.org/resources/'
                 'campus-sustainability-policy-bank/')},
    ]
}


def main():
    for parent_name, children in categories.items():
        parent_category = Category.objects.create(name=parent_name)
        for child in children:
            Category.objects.create(parent=parent_category,
                                    name=child['name'],
                                    url=child['url'])


def backfill():
    for parent_name, children in categories.items():
        for child in children:
            child_category = Category.objects.filter(name=child['name'])[0]
            child_category.url = child['url']
            child_category.save()


if __name__ == '__main__':
    main()
